# Railway Deployment Guide

## 🚀 Deploy to Railway

This Reflex application is configured for easy deployment on Railway.

### Prerequisites

- Railway account (https://railway.app)
- Git repository (GitHub, GitLab, etc.)

### Quick Deploy

1. **Push to Git**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Connect to Railway**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect the Dockerfile and deploy

3. **Configure Environment**
   - Railway will automatically use the `Dockerfile`
   - The app will bind to Railway's `$PORT` variable
   - No additional environment variables needed for basic deployment

4. **Access Your App**
   - Railway will provide a public URL
   - Your app will be live at `https://<your-app>.railway.app`

### Deployment Configuration

#### Dockerfile
The included `Dockerfile`:
- Uses Python 3.11 slim image
- Installs Node.js 18 for frontend compilation
- Installs all dependencies from `requirements.txt`
- Exports Reflex frontend for production
- Runs backend server on Railway's dynamic port

#### .dockerignore
Excludes:
- `__pycache__/` and `.pyc` files
- Virtual environments (`venv/`, `env/`)
- `.web/` (regenerated during build)
- IDE and OS files
- Git history

### Environment Variables (Optional)

If you need to customize the deployment, add these in Railway's dashboard:

- `BACKEND_HOST` - Default: `0.0.0.0`
- `BACKEND_PORT` - Default: Railway's `$PORT`
- `PYTHONUNBUFFERED` - Default: `1` (set automatically)

### Post-Deployment

After deployment, your app will:
- Fetch user location via GeoIP (ipapi.co)
- Display interactive star map background
- Show latest ham radio contact from logbook
- Display current weather for KHNZ with alerts

### Updating the Deployment

To update your deployed app:

```bash
git add .
git commit -m "Your update message"
git push
```

Railway will automatically rebuild and redeploy.

### Custom Domain (Optional)

1. Go to your Railway project settings
2. Click on "Domains"
3. Add your custom domain
4. Update your DNS records as instructed

### Troubleshooting

#### Build Fails
- Check Railway build logs
- Ensure all dependencies are in `requirements.txt`
- Verify Dockerfile syntax

#### App Won't Start
- Check Railway deployment logs
- Ensure `reflex run` command is correct
- Verify port binding to `$PORT`

#### Features Not Working
- **Star Map**: Check browser console for d3-celestial errors
- **Weather**: Verify NWS API is accessible
- **Logbook**: Ensure hamlog.chancecallahan.com is reachable

### Development vs Production

**Local Development**:
```bash
reflex run
```

**Production (Railway)**:
```bash
reflex run --env prod --loglevel info --backend-host 0.0.0.0 --backend-port $PORT
```

### Performance Tips

1. **Caching**: Consider caching API responses (weather, logbook)
2. **CDN**: d3-celestial loads from CDN (already optimized)
3. **Database**: Add Redis for state persistence (optional)

### Monitoring

Railway provides:
- Real-time logs
- Resource usage metrics
- Deployment history
- Automatic HTTPS

### Cost

Railway offers:
- **Free tier**: $5 credit/month (plenty for this app)
- **Pro tier**: $20/month for more resources
- This app should run comfortably on free tier

### Support

- Railway Docs: https://docs.railway.app
- Reflex Docs: https://reflex.dev/docs/hosting/self-hosting/
- Issues: Create issue in your repository

---

## Alternative Deployment Options

### Docker Compose (Self-Hosted)

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
```

### Other Platforms

- **Render**: Similar to Railway, auto-detects Dockerfile
- **Fly.io**: Requires `fly.toml` configuration
- **DigitalOcean App Platform**: Deploy from GitHub directly
- **AWS/GCP/Azure**: Deploy container to cloud run/app service

---

**Happy Deploying! 🎉**
