import asyncio
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, NoteSerializer, ChatMessageSerializer
from django.conf import settings
from django.core.files.storage import default_storage
from .models import Note, ChatMessage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
import json
from .ai_agent.prompts import context
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.readers.file.docs.base import PDFReader
from .ai_agent.pdf import get_pdf_engines
from .ai_agent.news import news_engine
from .ai_agent.crypto import crypto_price_tool
from .ai_agent.weather import weather_engine
from .ai_agent.financial import financial_engine
from .ai_agent.stock_news import news_sentiment_tool_instance
from .ai_agent.topgainers import top_gainers_losers_tool
from .ai_agent.llm import get_llm, init_llama_settings
import os

# Load environment variables
load_dotenv()

dynamic_tools = {}

def get_base_tools():
    """Build the base tool list lazily to avoid import-time LLM init."""
    engines = get_pdf_engines()
    return [
        weather_engine,
        news_engine,
        crypto_price_tool,
        financial_engine,
        news_sentiment_tool_instance,
        top_gainers_losers_tool,
        QueryEngineTool(
            query_engine=engines["united"],
            metadata=ToolMetadata(
                name="united_states_population_data",
                description="This gives information that can help you answer a query about the United States the country, or other data that is in United_States.pdf.",
            ),
        ),
        QueryEngineTool(
            query_engine=engines["world"],
            metadata=ToolMetadata(
                name="world_population_data",
                description="This gives information that can help you answer a query about the World population, or other data that is in WorldPopulation.pdf.",
            ),
        ),
        QueryEngineTool(
            query_engine=engines["kaleb"],
            metadata=ToolMetadata(
                name="kaleb_data",
                description="This gives information that can help you answer a query about the Kaleb Resume pdf so you can help answer specific questions about kaleb and his resume.",
            ),
        ),
    ]


def load_dynamic_pdf_tools():
    """Load PDF tools from previously indexed documents."""
    init_llama_settings()
    llm = get_llm()
    pdf_tools = []
    index_dir = os.path.join(settings.MEDIA_ROOT, "indexes")

    if not os.path.exists(index_dir):
        return pdf_tools

    for folder_name in os.listdir(index_dir):
        folder_path = os.path.join(index_dir, folder_name)
        if os.path.isdir(folder_path):
            try:
                index = load_index_from_storage(
                    StorageContext.from_defaults(persist_dir=folder_path)
                )
                engine = index.as_query_engine(llm=llm)
                pdf_tools.append(
                    QueryEngineTool(
                        query_engine=engine,
                        metadata=ToolMetadata(
                            name=f"{folder_name}_pdf_data",
                            description=f"Data from the uploaded PDF file: {folder_name}",
                        ),
                    )
                )
            except Exception as e:
                print(f"⚠️ Failed to load index from {folder_path}: {e}")
    return pdf_tools


def ensure_dynamic_tools_loaded():
    if dynamic_tools:
        return
    for tool in load_dynamic_pdf_tools():
        dynamic_tools[tool.metadata.name] = tool
    if dynamic_tools:
        print("✅ Loaded tools:", list(dynamic_tools.keys()))


class UploadPDFView(APIView):
    """Handle PDF file uploads and indexing."""

    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response({"error": "No file provided"}, status=400)

        filename = file_obj.name
        save_path = os.path.join(settings.MEDIA_ROOT, "pdfs", filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with default_storage.open(save_path, "wb+") as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        try:
            # Index PDF
            init_llama_settings()
            llm = get_llm()
            documents = PDFReader().load_data(file=save_path)
            clean_name = os.path.splitext(filename)[0].lower().replace(" ", "_")
            index_name = f"{clean_name}_index"
            index_dir = os.path.join(settings.MEDIA_ROOT, "indexes", index_name)

            index = VectorStoreIndex.from_documents(documents, show_progress=True)
            index.storage_context.persist(persist_dir=index_dir)

            query_engine = index.as_query_engine(llm=llm)
            tool = QueryEngineTool(
                query_engine=query_engine,
                metadata=ToolMetadata(
                    name=index_name,
                    description=f"A tool for answering questions about {filename}.",
                ),
            )

            dynamic_tools[index_name] = tool

            return Response(
                {"message": "PDF uploaded and indexed successfully", "index_name": filename},
                status=200,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class AIQueryView(views.APIView):
    """Handle AI chat queries using Google GenAI."""

    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = request.data
        user_input = data.get("prompt")
        if not user_input:
            return Response({"error": "No input provided"}, status=400)

        try:
            init_llama_settings()
            llm = get_llm()

            # Fetch user's chat history for context
            chat_history = ChatMessage.objects.filter(user=request.user).order_by("timestamp")
            chat_context = "\n".join(
                [f"User: {msg.message}\nBot: {msg.response}" for msg in chat_history]
            )

            # Create a new prompt with chat history
            full_prompt = f"{chat_context}\nUser: {user_input}" if chat_context else user_input

            # Use the full prompt with the agent
            ensure_dynamic_tools_loaded()
            base_tools = get_base_tools()
            combined_tools = base_tools + list(dynamic_tools.values())
            dynamic_agent = ReActAgent(
                tools=combined_tools,
                llm=llm,
                system_prompt=context,
                verbose=True,
                streaming=False,
            )

            async def _run_agent():
                handler = dynamic_agent.run(
                    user_msg=full_prompt,
                    max_iterations=10,
                    early_stopping_method="generate",
                )
                return await handler

            result = asyncio.run(_run_agent())
            response_message = getattr(result, "response", None)
            response_text = (
                response_message.content if response_message is not None else str(result)
            )

            # Store chat message
            ChatMessage.objects.create(
                user=request.user, message=user_input, response=response_text
            )

            return JsonResponse({"response": response_text})

        except RuntimeError as e:
            return Response(
                {"error": f"LLM configuration error: {e}"},
                status=500,
            )
        except Exception as e:
            error_message = str(e)
            if "safety" in error_message.lower() or "blocked" in error_message.lower():
                return Response(
                    {
                        "error": "The response was filtered due to content policies. Please try rephrasing your request."
                    },
                    status=400,
                )
            return Response({"error": error_message}, status=500)


class UserChatHistoryView(views.APIView):
    """Retrieve user's chat history."""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        chat_messages = ChatMessage.objects.filter(user=request.user).order_by("timestamp")
        serializer = ChatMessageSerializer(chat_messages, many=True)
        return Response(serializer.data)


class ClearChatHistoryView(views.APIView):
    """Clear user's chat history."""

    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        ChatMessage.objects.filter(user=request.user).delete()
        return Response(status=204)


class NoteListCreate(generics.ListCreateAPIView):
    """List and create notes for the authenticated user."""

    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class NoteDelete(generics.DestroyAPIView):
    """Delete a note for the authenticated user."""

    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)


class CreateUserView(generics.CreateAPIView):
    """Create a new user account."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
