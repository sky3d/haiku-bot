.PHONY: help clean zip deploy logs

help:
	@echo "Доступные команды:"
	@echo "  make zip     - Создать function.zip для деплоя"
	@echo "  make clean   - Удалить function.zip"
	@echo "  make deploy  - Задеплоить через gcloud CLI"
	@echo "  make logs    - Посмотреть логи функции"

clean:
	@rm -f function.zip
	@echo "✓ function.zip удален"

zip: clean
	@echo "Создание function.zip..."
	@zip -r function.zip . \
		-x "*.git*" ".git/*" \
		-x "*.env*" ".env" \
		-x "*.pyc" "__pycache__/*" \
		-x "*.md" "Makefile" \
		-x ".DS_Store" \
		-x ".idea/*" "*.idea*" \
		-x ".venv/*" "venv/*" \
		-x ".gcloudignore" ".gitignore" ".cloudignore" \
		-x "function.zip"
	@echo "✓ function.zip создан"

deploy:
	@if [ -z "$$TOKEN" ]; then \
		echo "❌ Установите переменные окружения:"; \
		echo "  export TOKEN=your_telegram_token"; \
		echo "  export CALENDAR_IMAGE_HOST=https://your-image-host"; \
		echo "  export VESNA_IMAGE_ENABLED=yes"; \
		echo ""; \
		echo "Пример:"; \
		echo "  export TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"; \
		echo "  export CALENDAR_IMAGE_HOST=https://thumb.cloud.mail.ru/weblink/thumb/xw1/gzzE/11DsMfgaq"; \
		echo "  export VESNA_IMAGE_ENABLED=yes"; \
		exit 1; \
	fi
	@echo "🚀 Деплой classic-haiku-bot..."
	gcloud functions deploy classic-haiku-bot \
		--runtime=python312 \
		--region=us-central1 \
		--source=. \
		--entry-point=handler \
		--trigger-http \
		--allow-unauthenticated \
		--set-env-vars TOKEN="$$TOKEN",CALENDAR_IMAGE_HOST="$$CALENDAR_IMAGE_HOST",VESNA_IMAGE_ENABLED="$$VESNA_IMAGE_ENABLED"

logs:
	@echo "📋 Логи classic-haiku-bot..."
	gcloud functions logs read classic-haiku-bot --region=us-central1 --limit=50
