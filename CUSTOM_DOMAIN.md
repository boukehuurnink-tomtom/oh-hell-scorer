# Custom Domain Setup for Oh Hell Score Recorder

You have several options to host your Oh Hell app at `www.bouke.eu/ohhell` or similar.

---

## Option 1: Subdomain (Recommended - Easiest)

**URL: `ohhell.bouke.eu`**

This is the simplest and most common approach.

### Steps:

1. **In Railway Dashboard:**
   - Go to your Oh Hell app
   - Click "Settings" → "Networking"
   - Click "Add Custom Domain"
   - Enter: `ohhell.bouke.eu`
   - Railway will give you a CNAME target (e.g., `xyz.up.railway.app`)

2. **In Telartis/Your DNS Provider:**
   - Log into your DNS management panel
   - Add a CNAME record:
     - **Type:** CNAME
     - **Name:** `ohhell`
     - **Target:** (the Railway CNAME from step 1)
     - **TTL:** 3600 (or default)
   - Save the record

3. **Wait for Propagation:**
   - DNS changes take 5-60 minutes
   - Railway will auto-detect and issue SSL certificate
   - Your app will be live at `https://ohhell.bouke.eu`

**Benefits:**
- ✅ Easy to set up
- ✅ Automatic HTTPS
- ✅ No additional servers needed
- ✅ Professional subdomain

---

## Option 2: Subdirectory with Reverse Proxy

**URL: `www.bouke.eu/ohhell`**

This requires you to have a web server running at `www.bouke.eu` that can proxy requests.

### Requirements:
- Web server at `bouke.eu` (Apache, Nginx, or hosting control panel)
- Access to server configuration
- Ability to set up reverse proxy

### If You Have a Web Server (Apache):

Add to your Apache config or `.htaccess`:

```apache
<Location /ohhell>
    ProxyPreserveHost Off
    ProxyPass https://web-production-3cc08.up.railway.app/
    ProxyPassReverse https://web-production-3cc08.up.railway.app/
</Location>
```

### If You Have Nginx:

Add to your Nginx config:

```nginx
location /ohhell/ {
    proxy_pass https://web-production-3cc08.up.railway.app/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### Challenges:
- ❌ Requires web server access
- ❌ More complex setup
- ❌ May break Flask sessions
- ❌ Static file paths may need adjustment
- ❌ Requires ongoing maintenance

**Note:** This is significantly more complex and may not work well with Flask's session handling.

---

## Option 3: Subdirectory with Path Rewriting

If you control `www.bouke.eu` and want the path approach, you'd need to:

1. Modify Flask app to handle a base path
2. Set up reverse proxy with path rewriting
3. Update all static file references

**This requires code changes:**

```python
# app.py modifications needed
app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/ohhell'

# Would also need to update all URL generation
# and static file references
```

---

## Option 4: Simple Redirect Page

**URL: `www.bouke.eu/ohhell` → redirects to `ohhell.bouke.eu`**

Create a simple HTML page at `www.bouke.eu/ohhell/index.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url=https://ohhell.bouke.eu">
    <title>Oh Hell Score Recorder</title>
</head>
<body>
    <p>Redirecting to <a href="https://ohhell.bouke.eu">Oh Hell Score Recorder</a>...</p>
</body>
</html>
```

**Benefits:**
- ✅ Simple to implement
- ✅ Users still get to app
- ✅ Maintains clean URL in browser
- ✅ No complex configuration

---

## Option 5: Use Railway's Custom Domain + Frame

Keep your Railway app but create a frame page at `www.bouke.eu/ohhell`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Oh Hell Score Recorder</title>
    <style>
        body, html { margin: 0; padding: 0; height: 100%; overflow: hidden; }
        iframe { width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>
    <iframe src="https://ohhell.bouke.eu"></iframe>
</body>
</html>
```

**Note:** Frames can have UX issues (back button, deep linking)

---

## My Recommendation: Subdomain (Option 1)

**Use: `ohhell.bouke.eu`**

### Why?
1. **Simple:** Just add a CNAME record
2. **Professional:** Clean, memorable URL
3. **Automatic HTTPS:** Railway handles SSL
4. **No server needed:** Works with Railway directly
5. **Fast setup:** 5 minutes
6. **Reliable:** No proxy complexity

### Setup Time: ~5 minutes

### Step-by-Step Guide:

#### A. In Railway:
1. Open your Oh Hell app
2. Click "Settings" tab
3. Scroll to "Networking"
4. Click "Custom Domain"
5. Enter: `ohhell.bouke.eu`
6. Copy the CNAME target Railway provides

#### B. In Your DNS (Telartis):
1. Log into Telartis control panel
2. Find DNS management for `bouke.eu`
3. Add new record:
   - **Type:** CNAME
   - **Host/Name:** `ohhell`
   - **Points to:** (paste Railway CNAME)
   - **TTL:** 3600
4. Save

#### C. Wait & Verify:
1. Wait 10-30 minutes for DNS propagation
2. Visit: `https://ohhell.bouke.eu`
3. Railway auto-issues SSL certificate
4. Done! 🎉

---

## Alternative: Root Domain

If you don't use `www.bouke.eu` for anything else, you could use:
- `ohhell.bouke.eu` (subdomain - recommended)
- `play.bouke.eu` (alternative)
- `cards.bouke.eu` (alternative)
- `games.bouke.eu/ohhell` (needs web server)

---

## DNS Provider Info

Since your domain is with **Telartis**, you'll need to:

1. **Log into Telartis**
2. **Find DNS Management** (might be called "DNS Settings", "Nameservers", "Zone File Editor")
3. **Look for existing records** for `bouke.eu`
4. **Add CNAME record** as described above

**Telartis typically provides:**
- DNS management interface
- CNAME record support
- TTL configuration
- SSL certificate support (if hosting with them)

---

## Checking DNS Propagation

After adding your CNAME record, check if it's working:

```bash
# On Mac/Linux
dig ohhell.bouke.eu

# On Windows
nslookup ohhell.bouke.eu

# Online tool
# Visit: https://dnschecker.org
# Enter: ohhell.bouke.eu
```

---

## Email Considerations

Your Google Business email setup won't be affected by adding a subdomain CNAME record. 

Your existing MX records (mail exchange) will remain intact:
- `mail.bouke.eu` → Google
- `@bouke.eu` email → Still works

Adding `ohhell.bouke.eu` won't interfere with email at all.

---

## Cost

**No additional cost!**
- ✅ Railway: Already free tier or existing plan
- ✅ DNS: Already included with Telartis
- ✅ SSL: Automatic and free via Railway
- ✅ Bandwidth: Included in Railway plan

---

## Summary Table

| Option | URL | Difficulty | SSL | Maintenance |
|--------|-----|------------|-----|-------------|
| **Subdomain** | `ohhell.bouke.eu` | ⭐ Easy | ✅ Auto | ✅ None |
| Subdirectory | `bouke.eu/ohhell` | ⭐⭐⭐⭐ Hard | ⚠️ Complex | ❌ High |
| Redirect | `bouke.eu/ohhell` → subdomain | ⭐⭐ Medium | ✅ Auto | ✅ Low |

---

## Quick Start (5 Minutes)

**Best approach for `bouke.eu` owner:**

1. **Railway:** Add custom domain `ohhell.bouke.eu`
2. **Telartis:** Add CNAME record pointing to Railway
3. **Wait:** 10-30 minutes for DNS
4. **Done:** Visit `https://ohhell.bouke.eu`

**Result:**
- Professional URL
- Automatic HTTPS
- Fast and reliable
- Easy to remember and share

🎯 **Recommended URL:** `https://ohhell.bouke.eu`

---

## Need Help?

If you need specific help with Telartis DNS settings:
1. Log into Telartis control panel
2. Look for "DNS" or "Domain Management"
3. Take a screenshot if you need guidance
4. The CNAME record is all you need!
