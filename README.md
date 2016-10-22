# munki-rebrand

Based on a script used by University of Oxford IT Services to rebrand [Munki](https://github.com/munki) for their *Orchard* branded Mac management solution, originally based on the [munki_rebrand.py script](https://gist.github.com/bochoven/c1c656e0c2e1b1078dfd) by [Arjen van Bochoven](https://github.com/bochoven) 

I didn't need a lot of what Oxford & Arjen were rebranding (yet).  Instead I needed a script that would take a bunch of post_install-\* scripts and generate a single "unified" installer for each post-install script that would set common settings for our munki service as well as set the client-identifier to a use a specific manifest (for each departmental ITPro).

If you're familiar with Munki it's better to just download the latest release and run either a second installer or script to modify it after the fact.  If you're handing it out to others (e.g. other ITPros just getting started with munki, or instructing users with admin access to install it) then a single installer that does it all is much less error prone.

There are other, potentially better ways:  as outlined here:  https://groups.google.com/forum/#!searchin/munki-dev/single$20munki$20installer%7Csort:relevance/munki-dev/5vZGG43d-5Q/qQ43b6kwBAAJ

Many thanks to Arjen & the folks at University of Oxford.  Feedback on how to cleanup the code greatefully accepted.

# What it does / does differently from Oxford & Arjen's version

Looks for any files (bash scripts) in the same directory it is running in starting with *postinstall_script-* (e.g. postinstall_script-math-default, postinstall_script-math-labs, postinstall_script-english-faculty)

If there's an existing munki subdirectory, doesn't nuke it but rather uses git to clear out any untracked directories and files (e.g. the postinstall_script-\* that may be left over from a previous run), then updates with the remote munki repo on github.  This could use being cleaned up by a more knowlegeable python programer git-master, I had to use "shell=True" to get it to work without requiring getting/installing gitpython libraries.  

And at the end it renames the resultant installer to department-munkitools-version-numbers.pkg  It probably should be munkitools-version-site-client-identifier.pkg but it does what I need.
