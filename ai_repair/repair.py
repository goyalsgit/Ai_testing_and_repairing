def generate_repairs(bugs):
    repairs = []
    for bug in bugs:
        # Simple repair suggestion based on bug description
        if 'tool not found' in bug['description'].lower():
            suggestion = "Install required tools (KLEE, clang) to enable symbolic execution."
        elif 'compilation failed' in bug['description'].lower():
            suggestion = "Check code syntax and ensure all dependencies are included."
        else:
            suggestion = f"Review and fix the issue at {bug['location']}: {bug['description']}"
        repairs.append({
            'bugId': None,  # Would be set in DB
            'suggestion': suggestion,
            'applied': False
        })
    return repairs
