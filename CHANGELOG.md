# Changelog

All notable changes to Souline are documented here.

## [1.0.0] - 2026-11-23

First stable release, renamed from AudioFerry.

### Fixed
- Audio dropouts during long sessions. The speaker latency could be set as low as one frame, far below the 250 ms minimum that AirPlay 2 receivers such as HomePod advertise, so late packets were dropped. Latency is now kept between 250 ms and 1.5 s.
- Packet pacing: the Windows timer resolution is raised to 1 ms while Souline runs, so RAOP packets are sent at steadier intervals.

### Added
- Speaker latency is shown and entered in milliseconds. Modes: Instant 250 ms, Responsive 500 ms, Balanced 1 s, Stable 1.5 s.
- Opt-in "Experimental: 0 ms latency" setting for users who prefer the lowest delay over long-session stability.
- Receiver-side timing warnings from pyatv are written to `bridge.log`.
- Windows 11 style interface (Sun Valley theme) that follows the Windows light/dark setting; advanced settings moved to their own tab and the window sizes itself to its content.
- Per-user installer (`Souline-Setup-v1.0.0.exe`) with Start menu shortcut and uninstaller.
- Settings and the start-with-Windows entry are migrated automatically from AudioFerry.

### Changed
- Default mode is Balanced (1 s) for new installations.
