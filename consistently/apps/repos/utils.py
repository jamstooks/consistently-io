def get_badge_name(pass_count, fail_count, waiting_count):

    name = "pending"

    if not waiting_count:
        name = "%d_%d" % (pass_count, pass_count+fail_count)

    return "consistently_%s.svg" % name
