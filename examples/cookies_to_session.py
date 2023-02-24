from api import TikTok

print(
    TikTok(
        session_id = TikTok().cookies_to_session(cookies = "store-idc=; store-country-code=; install_id=; ttreq=; passport_csrf_token=; passport_csrf_token_default=; multi_sids=; cmpl_token=; d_ticket=; uid_tt=; uid_tt_ss=; sid_tt=; sessionid=; sessionid_ss=; store-country-code-src=; tt-target-idc=; tt-target-idc-sign=; sid_guard=; msToken=; odin_tt=")
    ).edit_username(username = "newusername", user_id = 7198124813334990086))