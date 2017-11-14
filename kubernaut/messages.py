from click import style

GET_TOKEN_MSG = style("Kubernaut access token not configured. ") \
    + style("Please get a free access token continue:\n\n") \
    + style("https://kubernaut.io/token", bold=True, underline=True) \
    + style("\n\nAfterwards run `kubernaut set-token <TOKEN>`")
