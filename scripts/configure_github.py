"""Inspect, plan, optionally apply and verify repository settings using gh.

Dry-run is default. --offline-plan never contacts GitHub; it is useful without
administration credentials. Visibility and repository resources are never deleted.
"""
import argparse
import json
import subprocess

REPO = 'akin-demir/arabic-calligraphy-skill'
META = {'description':'20 Arabic calligraphy traditions for AI agents; honest font-based typography and RTL exports',
        'allow_squash_merge':False,'allow_merge_commit':True,'allow_auto_merge':False,
        'delete_branch_on_merge':False}
TOPICS = ['arabic-calligraphy','arabic-typography','agent-skills','codex','claude-code',
          'cursor','arabic-fonts','rtl','python','svg','pdf','open-source']
PROTECTION = {'required_status_checks':{'strict':True,'contexts':['quality','security']},
    'enforce_admins':True,'required_pull_request_reviews':{'required_approving_review_count':0},
    'restrictions':None,'allow_force_pushes':False,'allow_deletions':False}


def api(path,method='GET',body=None):
    cmd=['gh','api',path,'--method',method]
    if body is not None:
        cmd += ['--input','-']
    out=subprocess.run(cmd,input=json.dumps(body) if body is not None else None,
                       text=True,capture_output=True,check=False,timeout=30)
    if out.returncode:
        raise RuntimeError(out.stderr.strip())
    return json.loads(out.stdout) if out.stdout.strip() else None


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--offline-plan',action='store_true')
    args=parser.parse_args(argv)
    if args.offline_plan:
        print(json.dumps({'repository':REPO,'metadata':META,'topics':TOPICS,
                          'main_protection':PROTECTION,'applied':False},indent=2))
        return 0
    try:
        current=api(f'repos/{REPO}')
        changes={k:v for k,v in META.items() if current.get(k)!=v}
        topics=api(f'repos/{REPO}/topics')
        print('Metadata changes:',json.dumps(changes))
        print('Topic additions:',json.dumps(sorted(set(TOPICS)-set(topics.get('names',[])))))
        confirmed_absent=False
        api(f'repos/{REPO}/branches/main')
        try:
            existing=api(f'repos/{REPO}/branches/main/protection')
            print('Existing protection:',json.dumps(existing))
        except RuntimeError as error:
            print('Protection unavailable:',error)
            existing=None
            confirmed_absent='(HTTP 404)' in str(error)
        print('Proposed main protection:',json.dumps(PROTECTION))
        if not args.apply:
            print('Dry run. No settings were changed.')
            return 0
        if changes:
            api(f'repos/{REPO}','PATCH',changes)
        api(f'repos/{REPO}/topics','PUT',{'names':sorted(set(TOPICS)|set(topics.get('names',[])))})
        # Preserve non-targeted settings: never replace an existing protection policy.
        if existing is None and confirmed_absent:
            try:
                api(f'repos/{REPO}/branches/main/protection','PUT',PROTECTION)
            except RuntimeError as error:
                print('Protection was not applied:',error)
        else:
            print('Protection was preserved or inaccessible; review proposed policy manually.')
        verified=api(f'repos/{REPO}')
        assert all(verified.get(k)==v for k,v in META.items())
        verified_topics=api(f'repos/{REPO}/topics')
        assert set(TOPICS)<=set(verified_topics['names'])
        print('Metadata and topics verified. Verify protection separately in repository settings.')
        return 0
    except (RuntimeError,subprocess.TimeoutExpired) as error:
        print('Configuration not completed:',error)
        return 1


if __name__=='__main__':
    raise SystemExit(main())
