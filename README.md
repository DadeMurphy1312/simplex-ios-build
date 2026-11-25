# SimpleX Chat iOS build for TrollStore

Builds the unmodified SimpleX Chat v7.1.4 source at commit
`62ea5dc4afb73a0256ba0088f0ae85be750afc99` into an unsigned device app,
then applies an ad hoc signature and packages it as an IPA. This is a personal
build recipe, not an official SimpleX Chat release.

The GitHub Actions workflow builds the Haskell core with SimpleX's Nix iOS
recipe and builds the Swift app for `iphoneos`. The first build used the
upstream simulator CI's Cabal recipe; it started on the iPhone 6s but crashed
in the Haskell runtime at an unsupported `SWPAL` instruction. The Nix recipe
is the upstream iOS device build path, and its output must be checked on the
phone before calling the install working.

The IPA is meant for TrollStore on iOS 15. Push notifications may not work
without the developer's Apple push credentials. Test messaging while the app
is open before depending on it.
