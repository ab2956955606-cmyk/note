from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .schemas import GoalRequest, RagRequest, ReviewRequest
from .services.agent import PlannerAgent
from .services.rag import RagIndex

app = FastAPI(title="MyNotes AI Planner API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = PlannerAgent()
rag = RagIndex()


@app.get("/api/health")
def health():
    return {"ok": True, "service": "mynotes-ai"}


@app.post("/api/agent/plan")
async def generate_plan(req: GoalRequest):
    return await agent.plan(req)


@app.post("/api/agent/review")
async def review_day(req: ReviewRequest):
    return await agent.review(req)


@app.post("/api/rag/query")
async def query_materials(req: RagRequest):
    return rag.query(req)
