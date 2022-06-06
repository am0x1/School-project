// Kilde: https://anobjectisa.medium.com/javascript-service-worker-basics-254fc256e083

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('v1')
            .then(cache => {
                cache.addAll([
                    './fugl.jpeg',
                    './gruppemedlemmer.xml',
                    './index.asis',
                    './stil.css',
                    './styleweb.css',
                    './sw.js',
                    './test.css',
                    './test.html',
                    './test.xsl',
                    './typer.txt',
                    './webapp.html',
                    './webside.html',
                    './worker.js',
                    'http://localhost:8081/poems/poem/',
                ]);
                console.log("assets cached.");
            })
            .catch(err => console.log("could not cache."))
    )
});

self.addEventListener('fetch', event => {
    console.log("INTERCEPTED");

    event.respondWith(
        caches.match(event.request)
            .then(response => {
                console.log("V1 The request: ", event.request);
                console.log("V1 Got the response...", response);

                /* COMMENT OUT AND UNCOMMENT THESE EXAMPLES TO TEST THE RESULTS */

                /* EXAMPLE 1 */
                // from cache or fetched if not
                return response || fetch(event.request);
            })
            .catch(err => {
                console.log("Could not find matching request.");
                return null;
            })
    );
});