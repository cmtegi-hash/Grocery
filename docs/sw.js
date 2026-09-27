const CACHE_NAME = "lista-mercado-v1";
const ARCHIVOS = ["./index.html", "./manifest.json"];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ARCHIVOS))
  );
});

self.addEventListener("fetch", (event) => {
  // La lista (JSON de GitHub) siempre va directo a la red, nunca al caché.
  if (event.request.url.includes("lista_mercado.json")) {
    return;
  }
  event.respondWith(
    caches.match(event.request).then((res) => res || fetch(event.request))
  );
});
