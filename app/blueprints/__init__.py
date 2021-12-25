import app.blueprints.auth as auth

modules = (auth,)

blueprints = tuple(module.bp for module in modules)

def _get_hooks(module, before_or_after):
    return [hook for hook in getattr(module, f'{before_or_after}_hooks', [])]

before_hooks = tuple(item for sublist in [_get_hooks(module, 'before') for module in modules] for item in sublist)
after_hooks = tuple(item for sublist in [_get_hooks(module, 'after') for module in modules] for item in sublist)
