for sub in {1..$2}; do
    cd $sub

  for scan in {1..$6}; do
    cd $scan

    echo "--Import Functional Scan--"
        #Import from DICOM to AFNI
        for i in {1..$4}; do
          if [ ! -f run${i}+orig.HEAD ]; then
            run1TRs=`ls -1 raw/EPI_Run_*/*.dcm | wc -l` # Figure out how many TRs were in the run
            to3d -time:zt ${9} $run1TRs ${10} alt+z -prefix run${i} raw/EPI_Run_*/*.dcm
          fi
        done

    echo "--Import Structural Scan--"
        #Import structural scan
        if [ ! -f struct+orig.HEAD ]; then
          to3d -prefix struct raw/t1_mpr_sag_iso_*/*.dcm
        fi

    echo "--Co-register Structural to Functional--"
        #Co-register structural to functional
        3dWarp -oblique_parent run1+orig -prefix struct_rotated struct+orig

    echo "--Slice-time Correction--"
        #Slice-time correction
        3dTshift -verbose -prefix run1_shift run1+orig

    echo "--Motion Correction Within Functional Run--"
        #Motion correction within the run
        half3=$3/2
        3dvolreg -base run1_shift+orig'[$half3]' -prefix run1_volreg -1Dfile motion_1 run1_shift+orig

        cat motion_* >> motion.txt

    	#Output plot of motion.txt file to jpg file
    # 	1dplot -volreg motion.txt &

    echo "--Motion Censor File Creation--"
    	#Create the motion censor file
    	../../move_censor.pl

    echo "--Create Brain Mask--"
    	#Create the brain mask dataset
    	3dSkullStrip -input struct_rotated+orig -o_ply struct_brain
    	3dfractionize -template run1_volreg+orig. -input struct_brain+orig. -prefix struct_resamp
    	3dcalc -a struct_resamp+orig. -prefix struct_mask -expr "step(a)"

    echo "--Convert struct_rotated+orig to nifti--"
    	3dcopy struct_rotated+orig. struct_rotated.nii.gz

    echo "--Convert struct_brain+orig to nifti--"
      3dcopy struct_brain+orig. struct_brain.nii.gz

    cd ..
  done
  cd ..
done
