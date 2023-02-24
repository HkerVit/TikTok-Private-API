from api import TikTok

print(TikTok(session_id = None).followers_list(
        user_id = 6949066191752561669,
        sec_user_id = "MS4wLjABAAAAzmSxbYOMuhbJvmGDBTYlTYxyXMu7gDScJSi8IpuuoNn7miSgc1NJ_QKhS1Ea157L",
        count = 20
    )
)