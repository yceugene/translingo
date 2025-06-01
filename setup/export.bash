conda activate translingo
conda env export --from-history > env_base.yml     # Export only conda-installed packages (cleaner)
conda env export > full_env.yml                     # Export full environment including pip packages (may be verbose)
