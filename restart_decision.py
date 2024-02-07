def parse_conditions_file(filepath, name_dict):
    """

    :param filepath: path to conditions.txt
    :param name_dict: dictionary of sinner names and their pronouns, will be printed
    :return: a dictionary of the commands that can be understood by python
    """
    conditions = []
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if parts[0] == 'skill':
                conditions.append({
                    'type': 'skill',
                    'character': name_dict[parts[1]],
                    'skill': parts[2],
                    'slot': int(parts[3]) if len(parts) > 3 else None
                })
            elif parts[0] == 'speed':
                conditions.append({
                    'type': 'speed',
                    'character': name_dict[parts[1]],
                    'faster_than': [name_dict[name] for name in parts[2:]]
                })
            elif parts[0] == 'speed_value':
                conditions.append({
                    'type': 'speed_value',
                    'character': name_dict[parts[1]],
                    'value': int(parts[2])
                })
    return conditions


def check_restart_conditions(current_skills, conditions):
    """

    :param current_skills: the skills detected
    :param conditions: the conditions written in conditions.txt and parsed
    :return: boolean whether restart or not
    """
    for condition in conditions:
        if condition['type'] == 'skill':
            character, required_skill, slot = condition['character'], condition['skill'], condition.get('slot', None)
            if slot:  # If a specific slot is mentioned
                # Adjusting the index for slot to match Python's 0-based indexing.
                # Also ensure it checks up to the third slot.
                if current_skills[character][slot] != required_skill:
                    return True  # Skill in specified slot does not match.
            else:  # If no specific slot is mentioned, check all skill slots
                # Now checks all three skill slots.
                if not (required_skill in current_skills[character][1:4]):
                    return True

        elif condition['type'] == 'speed':
            base_character = condition['character']
            base_speed = current_skills[base_character][0]
            for other in condition['faster_than']:
                if base_speed >= current_skills[other][0]:
                    return True  # Speed condition not met.

        elif condition['type'] == 'speed_value':
            character = condition['character']
            required_speed = condition['value']
            if current_skills[character][0] < required_speed:
                return True  # Speed is less than required value, restart needed.

    return False  # All conditions met, no restart needed.
