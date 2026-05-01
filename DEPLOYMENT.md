# Deploying DocuGuard to Railway 🚀

DocuGuard is configured to deploy as a unified service on Railway. The FastAPI backend will serve the API endpoints and simultaneously host the static `index.html` landing page, keeping your infrastructure simple and cheap!

## Prerequisites
1. You need a GitHub account.
2. You need a [Railway](https://railway.app/) account.

## Step 1: Push to GitHub
First, initialize a git repository in your project folder, commit the files, and push them to a new GitHub repository:

```bash
cd /home/xc0mrade/Nim/docuguard
git init
git add .
git commit -m "Initial commit - DocuGuard V2"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

## Step 2: Create a Railway Project
1. Go to your Railway Dashboard.
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Select the repository you just created.
4. Click **Deploy Now**.

## Step 3: Configure Environment Variables (Optional but Recommended)
Railway will automatically detect the `Procfile` and `runtime.txt` and begin building the Python environment. While it's building:
1. Click on the newly created Service block in Railway.
2. Go to the **Variables** tab.
3. If you eventually add custom API keys or database connections, this is where you add them. (For now, the app uses hardcoded keys for the sandbox).

## Step 4: Generate a Public Domain
1. In the Service settings on Railway, go to the **Settings** tab.
2. Scroll down to **Networking** -> **Public Networking**.
3. Click **Generate Domain**. Railway will give you a free `up.railway.app` URL.

## Step 5: Test Your Deployment
Once the build completes (it will have a green checkmark):
1. Click on the generated Public Domain URL.
2. You should see your sleek new DocuGuard Landing Page!
3. Drag and drop an image into the playground section—the frontend is smart enough to automatically route the API call to your live Railway backend.

Done! You now have a production-ready API and Landing Page live on the internet.
