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
from .ai_agent.pdf import United_engine, World_engine, Kaleb_engine
from .ai_agent.news import news_engine
from .ai_agent.crypto import crypto_price_tool
from .ai_agent.weather import weather_engine
from .ai_agent.financial import financial_engine
from .ai_agent.stock_news import news_sentiment_tool_instance
from .ai_agent.topgainers import top_gainers_losers_tool
from llama_index.llms.openai import OpenAI
import openai
import os

# Load environment variables
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Define tools for the agent
tools = [

    weather_engine,
    news_engine,
    crypto_price_tool,
    financial_engine,
    news_sentiment_tool_instance,
    top_gainers_losers_tool,
    QueryEngineTool(query_engine=United_engine, metadata=ToolMetadata(
        name="united_states_population_data",
        description="This gives information that can help you answer a query about the United States the country, or other data that is in United_States.pdf.",
        ),
    ),
    QueryEngineTool(query_engine=World_engine, metadata=ToolMetadata(
        name="world_population_data",
        description="This gives information that can help you answer a query about the World population, or other data that is in WorldPopulation.pdf.",
        ),
    ),
    QueryEngineTool(query_engine=Kaleb_engine, metadata=ToolMetadata(
        name="kaleb_data",
        description="This gives information that can help you answer a query about the Kaleb Resume pdf so you can help answer specific questions about kaleb and his resume.",
        ),
    ),
]

# Initialize the LLM
llm = OpenAI(model="gpt-3.5-turbo-1106")

dynamic_tools = {}

# Initialize the ReActAgent
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context, max_iterations=10)

def load_dynamic_pdf_tools():
    tools = []
    index_dir = os.path.join(settings.MEDIA_ROOT, "indexes")

    for folder_name in os.listdir(index_dir):
        folder_path = os.path.join(index_dir, folder_name)
        if os.path.isdir(folder_path):
            try:
                index = load_index_from_storage(StorageContext.from_defaults(persist_dir=folder_path))
                engine = index.as_query_engine()
                tools.append(QueryEngineTool(
                    query_engine=engine,
                    metadata=ToolMetadata(
                        name=f"{folder_name}_pdf_data",
                        description=f"Data from the uploaded PDF file: {folder_name}"
                    )
                ))
            except Exception as e:
                print(f"⚠️ Failed to load index from {folder_path}: {e}")
    return tools

for tool in load_dynamic_pdf_tools():
    dynamic_tools[tool.metadata.name] = tool

print("✅ Loaded tools:", list(dynamic_tools.keys()))

class UploadPDFView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response({"error": "No file provided"}, status=400)

        filename = file_obj.name
        save_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with default_storage.open(save_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        try:
            # Index PDF
            documents = PDFReader().load_data(file=save_path)
            clean_name = os.path.splitext(filename)[0].lower().replace(" ", "_")
            index_name = f"{clean_name}_index"
            index_dir = os.path.join(settings.MEDIA_ROOT, 'indexes', index_name)

            index = VectorStoreIndex.from_documents(documents, show_progress=True)
            index.storage_context.persist(persist_dir=index_dir)

            query_engine = index.as_query_engine()
            tool = QueryEngineTool(
                query_engine=query_engine,
                metadata=ToolMetadata(
                    name=index_name,
                    description=f"A tool for answering questions about {filename}."
                )
            )

            dynamic_tools[index_name] = tool  # Register for agent later

            return Response({"message": "PDF uploaded and indexed successfully", "index_name": filename}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class AIQueryView(views.APIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = request.data
        user_input = data.get('prompt')
        if not user_input:
            return Response({'error': 'No input provided'}, status=400)
        
        try:
            # Fetch user's chat history
            chat_history = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
            chat_context = "\n".join([f"User: {msg.message}\nBot: {msg.response}" for msg in chat_history])
            
            # Create a new prompt with chat history
            full_prompt = f"{chat_context}\nUser: {user_input}"
            
            # Use the full prompt with the agent
            combined_tools = tools + list(dynamic_tools.values())
            dynamic_agent = ReActAgent.from_tools(combined_tools, llm=llm, verbose=True, context=context, max_iterations=10)

            result = dynamic_agent.chat(full_prompt)
            
            # Store chat message
            ChatMessage.objects.create(
                user=request.user,
                message=user_input,
                response=result
            )
            response_data = {'response': str(result)}  # Convert the result to a string
            return JsonResponse(response_data)
        except openai.BadRequestError:
            return Response({'error': 'The response was filtered due to content policies. Please try rephrasing your request or ask for different information.'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class UserChatHistoryView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        chat_messages = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
        serializer = ChatMessageSerializer(chat_messages, many=True)
        return Response(serializer.data)
    
class ClearChatHistoryView(views.APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        ChatMessage.objects.filter(user=request.user).delete()
        return Response(status=204)

class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
