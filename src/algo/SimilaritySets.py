def similarity(user, other_user, context):
    """The function of determining matching tags for two users.

    Args:
        user: The first user.
        other_user: The second user.
        context: The context for extracting tag values.

    Returns:
        Matching tags
    """
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

    tags = [context.get_message(t) for t in tags]
    return ", ".join(tags)
