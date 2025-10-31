# Деплой на Google Cloud Functions

## Способ 1: Через gcloud CLI (рекомендуется)

### Подготовка
```bash
# Установить переменные окружения
export PROJECT_ID="some-serverless"
export REGION="us-central1"
export FUNCTION_NAME="classic-haiku-bot"
```

### Деплой функции
```bash
gcloud functions deploy $FUNCTION_NAME \
  --gen2 \
  --runtime=python312 \
  --region=$REGION \
  --source=. \
  --entry-point=handler \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars TOKEN="your_telegram_token",CALENDAR_IMAGE_HOST="your-image-host"
```

### Получить URL функции
```bash
gcloud functions describe $FUNCTION_NAME --region=$REGION --gen2 --format="value(serviceConfig.uri)"
```

### Настроить Telegram Webhook
```bash
curl -X POST "https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=<FUNCTION_URL>"
```

---

## Способ 2: Через Google Cloud Console (ZIP)

### Подготовка архива
```bash
# Создать ZIP без .env, .git, .idea, .venv и других ненужных файлов
zip -r function.zip . -x "*.git*" ".git/*" "*.env*" ".env" "*.pyc" "__pycache__/*" "*.md" ".DS_Store" ".idea/*" "*.idea*" ".venv/*" "venv/*"
```

### Шаги в Console
1. Открыть [Cloud Functions](https://console.cloud.google.com/functions)
2. Нажать **CREATE FUNCTION**
3. Настройки:
   - **Environment**: 2nd gen
   - **Function name**: telegram-haiku-bot
   - **Region**: us-central1
   - **Trigger**: HTTPS
   - **Authentication**: Allow unauthenticated invocations
4. Нажать **NEXT**
5. **Runtime**: Python 3.12
6. **Source code**: ZIP upload
7. Загрузить `function.zip`
8. **Cloud Storage bucket**: выбрать `gcf-sources-*-us-central1` (bucket для Cloud Functions в вашем регионе)
9. **Entry point**: `handler`
9. В разделе **Runtime, build, connections and security settings**:
   - **Runtime environment variables**:
     - `TOKEN` = ваш токен
     - `CALENDAR_IMAGE_HOST` = https://thumb.cloud.mail.ru/weblink/thumb/xw1/gzzE/11DsMfgaq
10. Нажать **DEPLOY**

### После деплоя
Скопировать URL функции и настроить webhook:
```bash
curl -X POST "https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=<FUNCTION_URL>"
```

---

## Проверка работы

```bash
# Проверить статус функции
gcloud functions describe $FUNCTION_NAME --region=$REGION --gen2

# Посмотреть логи
gcloud functions logs read $FUNCTION_NAME --region=$REGION --gen2 --limit=50
```

## Обновление функции

```bash
# Просто повторить команду deploy
gcloud functions deploy $FUNCTION_NAME \
  --gen2 \
  --runtime=python312 \
  --region=$REGION \
  --source=. \
  --entry-point=handler \
  --trigger-http \
  --allow-unauthenticated \
  --update-env-vars TOKEN="new_token"
```
