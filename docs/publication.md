# Publish an Algorithm to `apex_algorithms` (Step-by-Step)

This is the shortest path to publish one algorithm from `openeo-udp` to `ESA-APEx/apex_algorithms`.

## 1) Prepare inputs in `openeo-udp`

1. Export final UDP JSON from the notebook.
2. Confirm the process graph runs on the target backend.
3. Prepare `preview.png` and `thumbnail.png`.
4. Confirm the notebook path you will link in the APEx record.

## 2) Create files in `apex_algorithms`

Assume `ALG=<algorithm_id>` (example: `bais2`).

1. Create folders:
`algorithm_catalog/developmentseed/$ALG/openeo_udp/`
`algorithm_catalog/developmentseed/$ALG/records/`
2. Add UDP JSON:
`algorithm_catalog/developmentseed/$ALG/openeo_udp/$ALG.json`
3. Add images:
`algorithm_catalog/developmentseed/$ALG/records/preview.png`
`algorithm_catalog/developmentseed/$ALG/records/thumbnail.png`
4. Add algorithm record:
`algorithm_catalog/developmentseed/$ALG/records/$ALG.json`

## 3) Fill algorithm record required links

In `algorithm_catalog/developmentseed/$ALG/records/$ALG.json`, include at minimum:

1. `application`: raw GitHub URL to UDP JSON in `apex_algorithms`.
2. `provider`: `../../record.json` (reuse Development Seed provider).
3. `platform`: relative link to platform record (for example `../../../../platform_catalog/titiler_openeo.json`).
4. `service`: backend base URL (for example `https://openeofed.dataspace.copernicus.eu`).
5. `webapp`: OpenEO Editor URL with `wizard~process`, `wizard~processUrl`, and `server`.
6. `notebook`: raw GitHub URL to notebook in `openeo-udp`.
7. `code`: `https://github.com/developmentseed/openeo-udp`.
8. `preview` and `thumbnail`: raw GitHub URLs to images in `apex_algorithms`.

## 4) Validate before PR

1. Provider record already exists:
`algorithm_catalog/developmentseed/record.json`
Do not create a new provider unless explicitly needed.
2. Platform record exists and matches the backend you linked.
If missing, add one under `platform_catalog/` and reference it from the algorithm record.
3. Check UDP parameter names match openEO process specs (BAIS2 required a fix here).
4. Confirm all record URLs are public and return `200`.
5. Confirm `webapp` `server=` matches the same backend as `service`.

## 5) PR workflow

1. Open PR from your branch in `apex_algorithms`.
2. During review, temporary branch URLs are acceptable if needed for testing.
3. Before merge, switch all temporary branch refs to `refs/heads/main` in:
- `application`
- `webapp` process URL
- `preview`
- `thumbnail`
4. Merge PR.

## BAIS2 lessons to always apply

1. Backend mismatch is easy to miss; keep `service` and `webapp server` aligned.
2. Branch-ref URLs often leak into merged records; clean them before merge.
3. Validate UDP argument naming/casing early to avoid late process-graph fixes.
