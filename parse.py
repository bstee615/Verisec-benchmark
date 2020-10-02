import re
from pathlib import Path

app_dirs = (a for a in Path('programs/apps').iterdir() if a.is_dir())
for app_dir in app_dirs:
    assert (app_dir / 'README').is_file()

    # print(f'{app_dir.name=}')
    
    readmes = list(app_dir.glob('**/README'))
    # print(f'{len(readmes)=}')
    
    bugs = []
    for readme in readmes:
        with readme.open('r') as f:
            text = f.read()
            match = re.match(r'-= ((CVE|BID|CA).*) =-', text)
            if match:
                cve = match.group(1)

                match = re.search(r'Vulnerable versions?:((.|\n)*)File(\(s\))?:((.|\n)*)Download from:((.|\n)*)Domain:(.*)\n', text)
                vulns = re.sub(r'\n\s+', ', ', match.group(1).strip())
                files = re.sub(r'\n\s+', ', ', match.group(4).strip())
                dl = match.group(6).strip()
                desc = f'Files: {files}, Download from: {dl}'
                # print(f'{vulns=}')

                bugs.append({
                    'cve': cve,
                    'vulns': vulns,
                    'desc': desc,
                })
            else:
                continue # This is the base readme
    # print(f'{cves=}')
    assert(len(bugs) == len(readmes) - 1)

    for bug in bugs:
        print(f'{app_dir.name}\t{bug["cve"]}\t{bug["vulns"]}\t{bug["desc"]}\t{bug["cve"]}')