from django.http import JsonResponse

from .database import execute_query


def people(request):
    try:
        query = """
        MATCH (p:Person)
        RETURN p.name AS name
        ORDER BY p.name
        """

        result = execute_query(query)

        if result is None:
            return JsonResponse(
                {"error": "Unable to connect to the database."},
                status=503
            )

        return JsonResponse(
            {"people": result},
            status=200
        )

    except Exception:
        return JsonResponse(
            {"error": "Something went wrong."},
            status=500
        )


def skills(request):
    try:
        query = """
        MATCH (s:Skill)
        RETURN s.name AS name
        ORDER BY s.name
        """

        result = execute_query(query)

        if result is None:
            return JsonResponse(
                {"error": "Unable to connect to the database."},
                status=503
            )

        return JsonResponse(
            {"skills": result},
            status=200
        )

    except Exception:
        return JsonResponse(
            {"error": "Something went wrong."},
            status=500
        )


def jobs(request):
    try:
        query = """
        MATCH (j:Job)
        RETURN j.title AS title
        ORDER BY j.title
        """

        result = execute_query(query)

        if result is None:
            return JsonResponse(
                {"error": "Unable to connect to the database."},
                status=503
            )

        return JsonResponse(
            {"jobs": result},
            status=200
        )

    except Exception:
        return JsonResponse(
            {"error": "Something went wrong."},
            status=500
        )


def companies(request):
    try:
        query = """
        MATCH (c:Company)
        RETURN c.name AS name
        ORDER BY c.name
        """

        result = execute_query(query)

        if result is None:
            return JsonResponse(
                {"error": "Unable to connect to the database."},
                status=503
            )

        return JsonResponse(
            {"companies": result},
            status=200
        )

    except Exception:
        return JsonResponse(
            {"error": "Something went wrong."},
            status=500
        )


def person_skills(request, name):
    try:
        query = """
        MATCH (p:Person {name: $name})-[:HAS_SKILL]->(s:Skill)
        RETURN s.name AS skill
        ORDER BY s.name
        """

        result = execute_query(
            query,
            {"name": name}
        )

        if result is None:
            return JsonResponse(
                {"error": "Unable to connect to the database."},
                status=503
            )

        return JsonResponse(
            {
                "person": name,
                "skills": result
            },
            status=200
        )

    except Exception:
        return JsonResponse(
            {"error": "Something went wrong."},
            status=500
        )


def recommendations(request, name):
    try:
        query = """
        MATCH (p:Person {name: $name})
              -[:HAS_SKILL]->(s:Skill)
              <-[:REQUIRES]-(j:Job)

        RETURN DISTINCT j.title AS job
        ORDER BY j.title
        """

        result = execute_query(
            query,
            {"name": name}
        )

        if result is None:
            return JsonResponse(
                {"error": "Unable to connect to the database."},
                status=503
            )

        return JsonResponse(
            {
                "person": name,
                "recommendations": result
            },
            status=200
        )

    except Exception:
        return JsonResponse(
            {"error": "Something went wrong."},
            status=500
        )


def company_recommendations(request, name):
    try:
        query = """
        MATCH (p:Person {name: $name})
              -[:HAS_SKILL]->(s:Skill)
              <-[:REQUIRES]-(j:Job)
              <-[:POSTED]-(c:Company)

        RETURN DISTINCT
               c.name AS company,
               j.title AS job

        ORDER BY c.name, j.title
        """

        result = execute_query(
            query,
            {"name": name}
        )

        if result is None:
            return JsonResponse(
                {"error": "Unable to connect to the database."},
                status=503
            )

        return JsonResponse(
            {
                "person": name,
                "matches": result
            },
            status=200
        )

    except Exception:
        return JsonResponse(
            {"error": "Something went wrong."},
            status=500
        )