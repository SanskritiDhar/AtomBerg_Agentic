# AtomBerg/nodes/report_generation.py
from langchain.chat_models import ChatOpenAI
from state import SoVState

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def report_node(state: SoVState) -> SoVState:
    prompt = f"""
    ### Share of Voice Report: {state.query}

    #### Basic SoV:
    {state.sov_results}

    #### Engagement-Weighted SoV:
    {state.engagement_sov_results}

    #### Positive SoV:
    {state.positive_sov_results}

    #### Negative SoV:
    {state.negative_sov_results}

    #### Platform-wise SoV:
    {state.platform_sov_results}

    Provide an analysis of brand dominance, sentiment balance, and platform-specific performance.
    """
    report = llm.predict(prompt)
    print(report)
    return state
