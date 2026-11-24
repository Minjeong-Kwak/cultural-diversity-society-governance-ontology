# Publication of CDSG 1.0.0-rc.2

## Persistent IRIs

All CDSG IRIs start with `https://w3id.org/cdsg/`. The redirect rules for w3id.org are in `w3id/ids/cdsg/.htaccess`, laid out as they go into a fork of `perma-id/w3id.org`. They follow the layout of the `adro` identifier.

| IRI | Redirects to |
|---|---|
| `/cdsg/core`, `/cdsg/core#Term` | core module of the current release, Turtle (RDF/XML on `Accept: application/rdf+xml`) |
| `/cdsg/core/1.0.0-rc.2` and other version IRIs | that module at the release tag `v1.0.0-rc.2` |
| `/cdsg/analytics`, `/cdsg/vocab`, `/cdsg/data` | the module of the current release |
| `/cdsg/merged` | the merged graph |
| `/cdsg/resource/...` | the evidence set |
| `/cdsg/shapes/core/`, `/target/`, `/actor-jurisdiction/` | the SHACL shapes |
| any IRI with `Accept: text/html` | the repository at the release tag |

Targets are files in the GitHub repository `Minjeong-Kwak/cultural-diversity-society-governance-ontology` at tag `v1.0.0-rc.2`, with the package root as the repository root.

`check_redirects.py` emulates the rules for every `w3id.org/cdsg` IRI in the release (1,012) and checks that each target exists in the package. The rules pass `w3id-check` (perma-id/w3id.org tools/check, 41 rules).

## Order of steps

1. Create the repository above, push this package as its root and tag the commit `v1.0.0-rc.2`.
2. In the fork `Minjeong-Kwak/w3id.org`, add `ids/cdsg/.htaccess` from this folder on a new branch and open a pull request to `perma-id/w3id.org`. w3id reviewers check that the targets resolve, so step 1 comes first.
3. At each new release, replace `1.0.0-rc.2` in the current-release rules (11 lines) and rerun `check_redirects.py`.
