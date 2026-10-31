# PDO SQLite can return a phantom row

![Library checkout cards illustrate a stale prefetched row and the empty result after reset.](infographic.png)

Issue: [php/php-src#25106](https://github.com/php/php-src/issues/25106).

This AI-generated illustration uses a library-card theme. The displayed JSON and labels were visually checked against the executed reproduction. The exact native image-generation prompt is in [prompt-used.txt](prompt-used.txt).

PDO lets an application prepare a SQLite query once and execute it with different parameters. The SQLite driver keeps track of a prefetched row until the application reads it or the cursor resets.

If the application executes a statement again while a previous row is unread, and the new execution has no rows, `fetchAll(PDO::FETCH_ASSOC)` can return `[{"answer":null}]` instead of `[]`. An explicit `closeCursor()` before the second execution also reproduces the problem.

The cursor resets the SQLite statement but leaves the `pre_fetched` flag set. The proposed fix clears that flag during the reset, so a later empty result stays empty.

The regression failed before the fix and passed afterward on PHP 8.7.0-dev at commit `248c5c45409667b5e69bba38a92c5cc9edd7582a`. The PDO SQLite and shared PDO tests reported 220 passes, 10 skips, one expected failure, and no unexpected failures. The patched build was tested on Linux NTS at that commit. The full PHP suite, other platforms, and release branches were not tested.

See the [public bug report](https://github.com/php/php-src/issues/25106) for the reproduction and related pull request.
