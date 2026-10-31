# JSON distinguishes a missing property from null

![Botanical specimen cards distinguish an uninitialized field, an omitted field, and explicit null.](infographic.png)

Issue: [php/php-src#25108](https://github.com/php/php-src/issues/25108).

This AI-generated illustration uses a botanical catalog theme. The JSON labels were visually checked against the executed reproduction. The exact native image-generation prompt is in [prompt-used.txt](prompt-used.txt).

`json_encode()` converts public object properties into JSON fields. A typed property that has not been initialized should be omitted from the output.

If that backed property has a setter hook, the encoder can include it as `{"id":null}` even though it has no value. For the uninitialized property in this example, the expected JSON is `{}`.

The proposed fix skips the internal uninitialized marker before writing the property name. A separate nullable property explicitly initialized to `null` still appears in JSON, as does a getter that returns `null`.

The regression failed before the fix and passed afterward on PHP 8.7.0-dev at commit `248c5c45409667b5e69bba38a92c5cc9edd7582a`. The JSON and property-hook tests reported 323 passes, five skips, and no failures. The patched build was tested on Linux NTS at that commit. The full PHP suite, other platforms, and release branches were not tested.

See the [public bug report](https://github.com/php/php-src/issues/25108) for the reproduction and related pull request.
