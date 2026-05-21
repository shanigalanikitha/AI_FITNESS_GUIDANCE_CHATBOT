def validate_user_input(question):

    # ================= EMPTY INPUT =================

    if not question.strip():

        return False, "Please enter a fitness question."

    # ================= VERY SHORT INPUT =================

    if len(question.strip()) < 3:

        return False, "Question is too short."

    # ================= VALID INPUT =================

    return True, "Valid Input"