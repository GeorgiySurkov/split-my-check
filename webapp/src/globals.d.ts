declare global {
  interface WebAppT {
    initDataUnsafe: InitDataT;
  }

  interface TelegramT {
    WebApp: WebAppT;
  }

  interface Window {
    Telegram: TelegramT;
  }
}

export {}
