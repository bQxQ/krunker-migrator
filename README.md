### Krunker migrator explained

1. **Login attempt**

   * You send username/email + password to Krunker’s login endpoint.
   * Instead, the API responds with:

     ```json
     { "type": "ensure_migrated", "challenge_id": "<some id>" }
     ```

   → This is Krunker saying: *“Before you can log in, you must migrate your account.”*

---

2. **Migration request**

   ```js
   axios.post(`https://gapi.svc.krunker.io/auth/migrate/${challengeId}`, { email })
   ```

   * You send a request to `auth/migrate/{challengeId}` with the **email** you want attached to the account.
   * If accepted, Krunker replies with something like:

     ```json
     { "type": "enter_code", "challenge_id": "<new id>" }
     ```

   → This means they sent a **verification code** to that email.

---

3. **Submit code**

   ```js
   axios.post(`https://gapi.svc.krunker.io/auth/code-challenge/${challengeId}`, { code })
   ```

   * You take the code from your email inbox and send it to the `code-challenge` endpoint.
   * If the code is valid, Krunker replies:

     ```json
     { "type": "login_ok", "access_token": "...", "refresh_token": "...", "login_token": "..." }
     ```

   → The account is now migrated and logged in.
