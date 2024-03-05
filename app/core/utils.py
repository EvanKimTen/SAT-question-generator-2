async def generate_category_string(categories: list, supabase) -> list:
    category_strings = []
    for category in categories:
        query = (
            supabase.from_("problem_categories")
            .select("level1, level2, level3")
            .eq("id", category)
        )

        result = query.execute()

        concatenated_string = f"{result.data[0]['level1']} {result.data[0]['level2'] or ''} {result.data[0]['level3'] or ''}"

        category_strings.append(concatenated_string)
    return category_strings


async def fetch_problems_by_category_ids(category_ids: list, supabase):
    problem_category_id_list = await get_problem_ids_by_category_ids(
        category_ids, supabase
    )

    problems_ids = supabase.table("problems").select("id, question").execute()
    problems_ids_data = problems_ids.data
    questions = []

    for category_id in problems_ids_data:
        for category_id_l in problem_category_id_list:
            if category_id["id"] == category_id_l:
                if category_id not in questions:
                    questions.append(category_id)

    return questions


async def get_problem_ids_by_category_ids(category_ids: list, supabase) -> list:
    """
    To retrieve the corresponding id to the given category,
    1. Retrieve level 1 categories
    2. Retrieve level 2 categories only if there's no specified depth.
    3. Match category IDs with the ones in the prob_cat_cat
    to return a list of their problem IDs.

    """
    problem_problem_categories = (
        supabase.table("problem_problem_categories")
        .select("problem_id, category_id")
        .execute()
    )

    # FIXME: ids will be string, temporarily change category_ids element to int
    # category_ids = list(map(int, category_ids))

    data = problem_problem_categories.data
    problem_category_dict = {}
    for d in data:
        if d["problem_id"] in problem_category_dict:
            problem_category_dict[d["problem_id"]].append(d["category_id"])
        else:
            problem_category_dict[d["problem_id"]] = [d["category_id"]]
    filtered_problem_ids = []
    for problem_id, category_list in problem_category_dict.items():
        if set(category_list) == set(category_ids):
            filtered_problem_ids.append(problem_id)

    return filtered_problem_ids
