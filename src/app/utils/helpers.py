def bounded_float(label, min_val, max_val):
    def check(val):
        f = float(val)
        if f < min_val or f > max_val:
            raise ValueError(f"{label} must be in [{min_val}, {max_val}]")
        return f

    return check
