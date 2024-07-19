import { createI18n } from 'vue-i18n';

const loadLocaleMessages = async () => {
  const locales = import.meta.glob('./language/config/*.json');
  const messages = {};

  for (const path in locales) {
    const matched = path.match(/\/([A-Za-z0-9-_]+)\./i);
    if (matched && matched.length > 1) {
      const locale = matched[1];
      const module = await locales[path](); // Await the import
      messages[locale] = module.default || module; // Access the default export or the module itself
    }
  }

  return messages;
};

const initI18n = async () => {
  const messages = await loadLocaleMessages();

  return createI18n({
    locale: import.meta.env.VITE_I18N_LOCALE || 'en',
    fallbackLocale: import.meta.env.VITE_I18N_FALLBACK_LOCALE || 'en',
    messages,
  });
};

export default initI18n;
