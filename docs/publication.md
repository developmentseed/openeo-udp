# Publishing openEO UDP algorithms to APEx

This guide describes how to publish an openEO UDP algorithm to the APEx Algorithm Catalogue using this repository. It is based on the BAIS2 onboarding flow and assumes you will use the existing Development Seed provider record (do not create a new provider).

## Overview

To publish an algorithm you will:

1. Export the openEO UDP JSON from your notebook or workflow.
2. Add the UDP JSON and any preview assets to this repository.
3. Create an OGC API Record for the service that links to the UDP JSON, preview images, provider, and platform.
4. Open a PR to the APEx repository.

We maintain an active fork for development work at:

`https://github.com/developmentseed/apex_algorithms`

## Prerequisites

- Your UDP process graph JSON is exported and validated on an openEO backend.
- You have preview images that demonstrate the output (e.g., burned area detection).
- You know the target APEx platform record to reference (example: `platform_catalog/openeo_platform.json`).

## Repository layout

Use the existing Development Seed provider folder:

- Provider record: `algorithm_catalog/developmentseed/record.json`

Add your algorithm under the provider directory:

- UDP definition: `algorithm_catalog/developmentseed/<algorithm>/openeo_udp/<algorithm>.json`
- OGC API Record: `algorithm_catalog/developmentseed/<algorithm>/records/<algorithm>.json`
- Optional assets: `algorithm_catalog/developmentseed/<algorithm>/records/preview.png` and `thumbnail.png`

## Steps

### 1) Add the openEO UDP JSON

Place the exported process graph JSON at:

`algorithm_catalog/developmentseed/<algorithm>/openeo_udp/<algorithm>.json`

Make sure the file name matches the UDP `id`.

### 2) Add preview assets

Add preview and thumbnail images under:

`algorithm_catalog/developmentseed/<algorithm>/records/`

Use PNGs with descriptive content that renders well in the catalogue.

### 3) Create the OGC API Record

Create a record at:

`algorithm_catalog/developmentseed/<algorithm>/records/<algorithm>.json`

Key fields to include:

- `properties.title`, `properties.description`, `properties.keywords`, `properties.license`
- `links` entries for:
  - `application` (publicly accessible UDP JSON URL)
  - `provider` (relative path: `../../record.json`)
  - `platform` (relative path to a platform record)
  - `preview` (preview image)
  - `thumbnail` (thumbnail image)
  - `about` (documentation or notebook)
  - `code` (repository link)

Follow the BAIS2 record for a complete example:

`algorithm_catalog/developmentseed/bais2/records/bais2.json`

### 4) Open a PR to APEx

1. Fork the repository.
2. Commit your changes.
3. Open a PR for review.

Once merged, the service will be visible in the APEx Algorithm Catalogue.

## Notes

- Do not create a new provider entry for Development Seed; reuse `algorithm_catalog/developmentseed/record.json`.
- Always include a `platform` link in the algorithm record that points to the platform your UDP runs on (e.g., `platform_catalog/titiler_openeo.json`).
- Keep links public and stable; avoid feature-branch or temporary URLs.
