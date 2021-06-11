BASE_API_PATH = "/api/v1"
DATABASE_URI = "postgres://kqejfycmueuecf:717cac44aaa9c449627083c73a063dab2f7a7cf7083ee18235537f651af4ad9d@ec2-50-19-176-236.compute-1.amazonaws.com:5432/df64s3e5darhft"

# View https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP for details
CONTENT_SECURITY_POLICY = {
    "default-src": " ".join(
        [
            "'self'",
        ]
    ),
    "script-src": " ".join(
        [
            "'self'",
            "'unsafe-inline'",  # to remove the unsafe-inline for extra safety, currently needed for the menu bar.
            "'unsafe-eval'"  # from summary page.
            "https://cdn.jsdelivr.net/npm/vue/dist/vue.js",
        ]
    ),
    "style-src": " ".join(
        [
            "'self'",
            "'unsafe-inline'",
            "fonts.googleapis.com",
            "fonts.gstatic.com",
        ]
    ),
}
