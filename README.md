# SimpleX Chat iOS build for TrollStore

Builds the unmodified SimpleX Chat v7.1.4 source at commit
`62ea5dc4afb73a0256ba0088f0ae85be750afc99` into an unsigned device app,
then applies an ad hoc signature and packages it as an IPA. This is a personal
build recipe, not an official SimpleX Chat release.

The GitHub Actions workflow builds the Haskell core with SimpleX's own
`scripts/ci/ios-sim/build-core.sh`, prepares the iOS static libraries with
`scripts/ci/ios-sim/prepare-libs.sh`, and builds the Swift app for `iphoneos`.

The IPA is meant for TrollStore on iOS 15. Push notifications may not work
without the developer's Apple push credentials. Test messaging while the app
is open before depending on it.
