from click import style

GET_TOKEN = style("Kubernaut access token not configured. ") \
            + style("Please get a free access token continue:\n\n") \
            + style("https://kubernaut.io/token", bold=True, underline=True) \
            + style("\n\nAfterwards run `kubernaut set-token <TOKEN>`")

VERSION_OUTDATED = "Your version of %(prog)s is out of date! The latest version is {0}." \
                   + " Please go to " + style("https://github.com/datawire/kubernaut", underline=True) \
                   + " for update instructions."
