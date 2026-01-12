"""
CLI Interface for InternHub AI Platform
"""

import typer
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from models import StudentProfile, InternshipDescription
from ai_engine import AIEngine

app = typer.Typer(help="InternHub AI Platform - CLI Interface")
console = Console()
ai_engine = AIEngine()


@app.command()
def match(
    profile: Path = typer.Option(
        None, "--profile", "-p", help="Path to student profile JSON"
    ),
    internship: Path = typer.Option(
        None, "--internship", "-i", help="Path to internship description JSON"
    ),
    interactive: bool = typer.Option(False, "--interactive", help="Interactive mode"),
):
    """
    Match a student profile with an internship description
    """

    if interactive:
        console.print("[bold cyan]InternHub AI - Interactive Mode[/bold cyan]\n")
        student = get_profile_interactive()
        intern = get_internship_interactive()
    else:
        if not profile or not internship:
            console.print(
                "[red]Error: Provide --profile and --internship paths, or use --interactive[/red]"
            )
            raise typer.Exit(1)

        # Load from files
        try:
            with open(profile) as f:
                student_data = json.load(f)
                student = StudentProfile(**student_data)

            with open(internship) as f:
                intern_data = json.load(f)
                intern = InternshipDescription(**intern_data)
        except Exception as e:
            console.print(f"[red]Error loading files: {e}[/red]")
            raise typer.Exit(1)

    # Perform matching
    console.print("\n[yellow]Analyzing match...[/yellow]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Processing with AI...", total=None)

        try:
            result = ai_engine.generate_complete_match(student, intern)
            progress.update(task, completed=True)
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
            raise typer.Exit(1)

    # Display results
    display_results(result, student, intern)


def get_profile_interactive() -> StudentProfile:
    """Get student profile interactively"""
    console.print("[bold]Student Profile[/bold]")

    name = typer.prompt("Name")
    email = typer.prompt("Email (optional)", default="")
    education = typer.prompt("Education (e.g., 'BS Computer Science, Junior')")

    skills_input = typer.prompt("Skills (comma-separated)")
    skills = [s.strip() for s in skills_input.split(",")]

    interests_input = typer.prompt("Interests (comma-separated)")
    interests = [i.strip() for i in interests_input.split(",")]

    experience = typer.prompt("Experience (optional)", default="")

    projects_input = typer.prompt("Projects (comma-separated, optional)", default="")
    projects = (
        [p.strip() for p in projects_input.split(",")] if projects_input else None
    )

    return StudentProfile(
        name=name,
        email=email or None,
        education=education,
        skills=skills,
        interests=interests,
        experience=experience or None,
        projects=projects,
    )


def get_internship_interactive() -> InternshipDescription:
    """Get internship description interactively"""
    console.print("\n[bold]Internship Description[/bold]")

    title = typer.prompt("Title")
    company = typer.prompt("Company")
    description = typer.prompt("Description")

    requirements_input = typer.prompt("Requirements (comma-separated)")
    requirements = [r.strip() for r in requirements_input.split(",")]

    responsibilities_input = typer.prompt("Responsibilities (comma-separated)")
    responsibilities = [r.strip() for r in responsibilities_input.split(",")]

    return InternshipDescription(
        title=title,
        company=company,
        description=description,
        requirements=requirements,
        responsibilities=responsibilities,
    )


def display_results(result, student: StudentProfile, internship: InternshipDescription):
    """Display matching results in a beautiful format"""

    # Header
    console.print("\n" + "=" * 80)
    console.print(
        Panel.fit(
            f"[bold cyan]{student.name}[/bold cyan] × [bold green]{internship.title}[/bold green] at [bold yellow]{internship.company}[/bold yellow]",
            title="Match Results",
        )
    )

    # Scores
    score_table = Table(show_header=False, box=None)
    score_table.add_column(style="cyan")
    score_table.add_column(style="bold green")

    score_table.add_row("Overall Match Score:", f"{result.match_score:.1f}%")
    score_table.add_row("ATS Confidence Score:", f"{result.ats_confidence_score:.1f}%")

    console.print(Panel(score_table, title="📊 Scores", border_style="green"))

    # Match Summary
    console.print(
        Panel(result.match_summary, title="📝 Match Summary", border_style="blue")
    )

    # Strengths
    if result.strengths:
        strengths_text = "\n".join([f"✓ {s}" for s in result.strengths])
        console.print(
            Panel(strengths_text, title="💪 Your Strengths", border_style="green")
        )

    # Skill Gaps
    if result.skill_gaps:
        gaps_table = Table(show_header=True, header_style="bold magenta")
        gaps_table.add_column("Skill", style="yellow")
        gaps_table.add_column("Priority", style="red")
        gaps_table.add_column("Learning Resources", style="cyan")

        for gap in result.skill_gaps:
            resources = "\n".join([f"• {r}" for r in gap.learning_resources[:2]])
            gaps_table.add_row(gap.skill, gap.importance, resources)

        console.print(
            Panel(
                gaps_table, title="📚 Skill Gaps & Learning Path", border_style="yellow"
            )
        )

    # Recommendations
    console.print(
        Panel(result.recommendations, title="💡 Recommendations", border_style="cyan")
    )

    # ATS Breakdown
    if "breakdown" in result.keyword_analysis:
        breakdown = result.keyword_analysis["breakdown"]
        ats_table = Table(show_header=True, header_style="bold")
        ats_table.add_column("Component", style="cyan")
        ats_table.add_column("Score", style="green")

        ats_table.add_row("Skill Match", f"{breakdown['skill_match']:.1f}%")
        ats_table.add_row("Experience Match", f"{breakdown['experience_match']:.1f}%")
        ats_table.add_row("Education Match", f"{breakdown['education_match']:.1f}%")
        ats_table.add_row("Keyword Density", f"{breakdown['keyword_density']:.1f}%")

        console.print(
            Panel(ats_table, title="🎯 ATS Score Breakdown", border_style="magenta")
        )

    # Save resume option
    if typer.confirm("\nWould you like to save the tailored resume?"):
        filename = f"resume_{student.name.replace(' ', '_')}_{internship.company}.txt"
        with open(filename, "w") as f:
            f.write(result.tailored_resume)
        console.print(f"[green]✓ Resume saved to {filename}[/green]")

    console.print("\n" + "=" * 80 + "\n")


@app.command()
def version():
    """Show version information"""
    console.print("[bold cyan]InternHub AI Platform[/bold cyan] v1.0.0")
    console.print("AI-powered internship matching")


if __name__ == "__main__":
    app()
