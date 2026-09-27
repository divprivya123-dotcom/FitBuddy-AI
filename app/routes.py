from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from markdown_it import MarkdownIt

from app.database import get_all_users, get_user, init_db, save_user, update_plan
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.models import User
from app.schemas import FeedbackRequest, UserInput
from app.updated_plan import update_workout_plan


router = APIRouter()

templates = Jinja2Templates(directory="templates")
markdown = MarkdownIt("commonmark", {"html": False})


def render_plan_markdown(plan):
    return markdown.render(plan or "")


templates.env.filters["markdown"] = render_plan_markdown
init_db()


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={"request": request}
)


@router.post("/generate-workout")
async def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    try:
        data = UserInput(
            username=username.strip(), user_id=user_id.strip(), age=age,
            weight=weight, goal=goal, intensity=intensity
        )
        if get_user(data.user_id):
            raise ValueError("That User ID is already registered. Please use another one.")
        workout_plan = generate_workout_gemini(
            data.age, data.weight, data.goal, data.intensity, data.username
        )
        nutrition_tip = generate_nutrition_tip_with_flash(data.goal)
        user = save_user(User(
            username=data.username, user_id=data.user_id, age=data.age,
            weight=str(data.weight), goal=data.goal, intensity=data.intensity,
            original_plan=workout_plan, updated_plan="", nutrition_tip=nutrition_tip
        ))
    except (ValidationError, ValueError, RuntimeError) as error:
        return templates.TemplateResponse(
            request=request, name="index.html",
            context={"request": request, "error": str(error)}
        )
    except Exception:
        return templates.TemplateResponse(
            request=request, name="index.html",
            context={"request": request, "error": "Plan generation failed. Check your Gemini API key and try again."}
        )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "username": user.username,
            "user_id": user.user_id,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "workout_plan": user.original_plan,
            "nutrition_tip": user.nutrition_tip,
            "updated": False
        }
    )


@router.post("/submit-feedback")
async def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...)
):
    try:
        data = FeedbackRequest(user_id=user_id.strip(), feedback=feedback.strip())
    except ValidationError as error:
        return templates.TemplateResponse(request=request, name="result.html", context={
            "request": request, "error": "Please enter a valid User ID and feedback.",
            "user_id": user_id
        })
    user = get_user(data.user_id)
    if not user:
        return templates.TemplateResponse(request=request, name="index.html", context={
            "request": request, "error": "User ID not found. Please check it and try again."
        })
    try:
        revised_plan = update_workout_plan(user.original_plan, data.feedback)
        update_plan(data.user_id, revised_plan, data.feedback)
    except Exception:
        return templates.TemplateResponse(request=request, name="result.html", context={
            "request": request, "error": "The plan could not be updated. Check your Gemini API key and try again.",
            "username": user.username, "user_id": user.user_id, "age": user.age,
            "weight": user.weight, "goal": user.goal, "intensity": user.intensity,
            "workout_plan": user.original_plan,
            "nutrition_tip": user.nutrition_tip
        })

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "username": user.username, "user_id": user.user_id, "age": user.age,
            "weight": user.weight, "goal": user.goal, "intensity": user.intensity,
            "workout_plan": revised_plan,
            "nutrition_tip": user.nutrition_tip, "updated": True
        }
    )


@router.get("/view-all-users")
async def view_all_users(request: Request):

    users = get_all_users()

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "request": request,
            "users": users
        }
    )