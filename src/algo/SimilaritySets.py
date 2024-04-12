from src import bot


def similarity(user, other_user, context):
    tags = []
    if user.preferences_tags is not None and other_user.preferences_tags is not None:
        for user_tag in user.preferences_tags:
            for over_user_tag in other_user.preferences_tags:
                if user_tag == over_user_tag:
                    tags.append(over_user_tag)

    if user.restrictions_tags is not None and other_user.restrictions_tags is not None:
        for user_tag in user.restrictions_tags:
            for over_user_tag in other_user.restrictions_tags:
                if user_tag == over_user_tag:
                    tags.append(over_user_tag)

    if user.dietary is not None and other_user.dietary is not None:
        for user_tag in user.dietary:
            for over_user_tag in other_user.dietary:
                if user_tag == over_user_tag:
                    tags.append(over_user_tag)

    if user.interests_tags is not None and other_user.interests_tags is not None:
        for user_tag in user.interests_tags:
            for over_user_tag in other_user.interests_tags:
                if user_tag == over_user_tag:
                    tags.append(over_user_tag)

    tags = [context.getMessage(t) for t in tags]

    return ', '.join(tags)


# def similarity(set1, set2):
#     intersection = len(set1.intersection(set2))
#     union = len(set1.union(set2))
#     return 100 * (intersection / union if union != 0 else 0)
