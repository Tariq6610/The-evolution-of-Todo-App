# ruff: noqa
# type: ignore
def create_rag_agent() -> Agent:
    """
    Create and configure the RAG agent with function tools and Gemini model.

    Returns:
        Agent: Configured agent instance ready for use with Runner

    Raises:
        ValueError: If required environment variables are missing
        Exception: If agent initialization fails

    Examples:
        >>> agent = create_rag_agent()
        >>> from agents import Runner, SQLiteSession
        >>> session = SQLiteSession("user_123", "conversations.db")
        >>> result = await Runner.run(agent, "What is Physical AI?", session=session)
    """
    settings = get_settings()

    # Validate required settings
    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable is required")

    logger.info("Creating RAG agent with Gemini model via OpenAI-compatible endpoint...")

    try:
        # Initialize AsyncOpenAI client pointing to Gemini's OpenAI-compatible endpoint
        gemini_client = AsyncOpenAI(
            api_key=settings.gemini_api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

        # Get model name (strip 'gemini/' prefix if present)
        model_name = settings.llm_model
        if model_name.startswith("gemini/"):
            model_name = model_name[7:]  # Remove 'gemini/' prefix

        # Create OpenAIChatCompletionsModel with Gemini client
        model = OpenAIChatCompletionsModel(model=model_name, openai_client=gemini_client)
        logger.info(f"Initialized Gemini model via OpenAI-compatible endpoint: {model_name}")

        # Create agent with tools
        agent = Agent(
            name="Physical AI and Robotics Expert",
            instructions=AGENT_INSTRUCTIONS,
            model=model,
            tools=[check_topic_relevance, retrieve_documentation],
        )

        logger.info(
            "RAG agent created successfully with tools: check_topic_relevance, retrieve_documentation"
        )
        return agent

    except Exception as e:
        logger.error(f"Failed to create RAG agent: {str(e)}", exc_info=True)
        raise


# Global agent instance (created lazily)
_agent_instance = None


def get_rag_agent() -> Agent:
    """
    Get or create the global RAG agent instance.

    Returns:
        Agent: The global RAG agent instance

    Examples:
        >>> agent = get_rag_agent()
    """
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = create_rag_agent()
    return _agent_instance
