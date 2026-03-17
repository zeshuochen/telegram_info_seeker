#!/bin/bash
set -e

REPO_URL="https://github.com/zeshuochen/telegram_info_seeker.git"
BRANCH="claude/initial-setup-GUeCU"
INSTALL_DIR="$HOME/telegram_info_seeker"

echo "================================================"
echo "  Telegram Info Seeker - One-Click Deployment"
echo "================================================"
echo ""

# Install Docker if not present
if ! command -v docker &>/dev/null; then
    echo "[1/4] Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker "$USER"
    echo "Docker installed. You may need to log out and back in for group changes."
else
    echo "[1/4] Docker already installed, skipping."
fi

# Check docker compose (plugin or standalone)
if docker compose version &>/dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
elif command -v docker-compose &>/dev/null; then
    COMPOSE_CMD="docker-compose"
else
    echo "[1/4] Installing Docker Compose plugin..."
    sudo apt-get update -qq
    sudo apt-get install -y docker-compose-plugin
    COMPOSE_CMD="docker compose"
fi

# Clone or update repo
if [ -d "$INSTALL_DIR/.git" ]; then
    echo "[2/4] Updating existing repository..."
    cd "$INSTALL_DIR"
    git fetch origin "$BRANCH"
    git checkout "$BRANCH"
    git pull origin "$BRANCH"
else
    echo "[2/4] Cloning repository..."
    git clone -b "$BRANCH" "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# Configure .env
echo ""
echo "[3/4] Configuration"
echo "-------------------"

if [ -f "$INSTALL_DIR/.env" ]; then
    read -r -p "  .env already exists. Overwrite? [y/N] " overwrite
    overwrite="${overwrite,,}"
    if [ "$overwrite" != "y" ]; then
        echo "  Keeping existing .env"
        SKIP_ENV=true
    fi
fi

if [ "${SKIP_ENV}" != "true" ]; then
    read -r -p "  Enter your BOT_TOKEN (from @BotFather): " bot_token
    if [ -z "$bot_token" ]; then
        echo "ERROR: BOT_TOKEN cannot be empty."
        exit 1
    fi

    read -r -p "  Enter KEYWORDS to filter (comma-separated, leave empty to save all): " keywords

    cat > "$INSTALL_DIR/.env" <<EOF
BOT_TOKEN=${bot_token}
KEYWORDS=${keywords}
EOF
    echo "  .env created."
fi

# Start the bot
echo ""
echo "[4/4] Starting bot..."
cd "$INSTALL_DIR"
sudo $COMPOSE_CMD up -d --build

echo ""
echo "================================================"
echo "  Deployment complete!"
echo "================================================"
echo ""
sudo $COMPOSE_CMD ps
echo ""
echo "Useful commands:"
echo "  View logs    : cd $INSTALL_DIR && sudo $COMPOSE_CMD logs -f"
echo "  Stop bot     : cd $INSTALL_DIR && sudo $COMPOSE_CMD down"
echo "  Restart bot  : cd $INSTALL_DIR && sudo $COMPOSE_CMD restart"
echo "  Check status : cd $INSTALL_DIR && sudo $COMPOSE_CMD ps"
echo ""
echo "Add the bot to your Telegram group and send /start to verify it works."
