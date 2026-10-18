# Missing & partial — consolidated parity inventory

> **What this is.** The full list of MATLAB R2025b functions and options nk does **not
> yet** fully match. This catalog is the single canonical source of truth for parity gaps.
> These are **parity gaps, NOT defects** — a missing or partial function is a feature gap,
> not a bug in shipped code (see `bugs/README.md` for the defect catalog: `bug` / `stub` / `missing-output`).
>
> **Kinds here:**
> - **⚠️ partial** — implemented in NK, but a documented branch/option is deferred.
> - **❌ missing** — not implemented at all.
>
> **Individually tracked.** Notable gaps also have their own dedicated entries in `bugs/opened/<ns>/<fn>.md`:
> friedman, distribution-dispatchers, autocorr (stats); pmusic-peig, fillgaps,
> pspectrum, stmcb (signal); watershed, imfindcircles, corner (image); wpdec,
> wentropy/ddencmp, wenergy/upcoef, cwt, wavedec2-family, centfrq/scal2frq
> (wavelet); lqr/hinfnorm, care/dare, minreal, initial, allmargin, covar
> (control); analog-demodulators, syndtable (comm); numerical-integration-nd,
> ode-stiff (ode); funm, qz/gsvd (linalg); fsolve, nonlinear-lsq,
> constrained-solvers (optim). The rest are catalogued here.

## ⚠️ Partial — implemented with a deferred branch (0)

_All previously tracked partial functions (`colon`, `fillmissing`, `topkrows`, `genqammod`, `apskmod`, `mskmod`, `dpcmenco`, `lloyds`, `balance`, `eig`, `ellipord`, `firls`, `corr`, `nearcorr`, `mle`, `bootci`, `bootstrp`, `crossval`, `jackknife`, `anova2`, `cond_pnorm`) are now 100% implemented._

## ❌ Missing — not implemented (818)

### Builtin

**Graphics hard copy (fieldtest portion 1, mdadams book):** `print`
(figure-to-file, 12 uses in one 44-script book repo — the single most
common absent fn in plotting code), `shading`; `histogram` (binning
plot — reachable only after the graphics harvest filter was lifted,
surfaced by example_11.m once randn('seed') was fixed)

**MATLAB demo datasets (portion 1):** the bundled sample images/data
(`peppers.png`, `cameraman.tif`, `spine.mat`, …) referenced by textbook
code (`imread('peppers.png')`) — nk ships none; a distribution
question, not a code gap. Revisit if/when the project wants a data pack.

**Symbolic Math Toolbox:** `syms` (7 uses in the same portion; the whole
symbolic stack is out of scope — tracked here as a gap, not planned)
**Springer math books (fieldtest portion 10, 2026-09-05):** `ode23s`
(2 — covered by the ode-stiff entry), `ezplot`, `dsolve`, `saveas`,
`scramble` (communications), `ichol` (incomplete Cholesky).
(`inline` was here — implemented 2026-09-05 as a str2func wrapper.)

**Entering Commands:** `commandhistory`, `commandwindow`, `diary`, `more`

**Matrices and Arrays:** `combinations`

**Control Flow:** `parfor`

**Cell Arrays:** `cellplot`, `timetable`

**Function Handles:** `function_handle`

**Categorical Arrays:** `addcats`, `categorical`, `categories`, `combinations`, `countcats`, `iscategory`, `isordinal`, `isprotected`, `isundefined`, `mergecats`, `removecats`, `renamecats`, `reordercats`, `setcats`

**Tables / Timetables:** `addprop`, `computebygroup`, `convertvars`, `inner2outer`, `innerjoin`, `jointables`, `mergevars`, `outerjoin`, `parquetread`, `parquetwrite`, `pivot`, `pivottable`, `readtable`, `rmprop`, `rowfun`, `rows2vars`, `splitvars`, `stack`, `stackedplot`, `stacktablevariables`, `standardizemissing`, `table2timetable`, `timetable2table`, `unstack`, `unstacktablevariables`, `varfun`, `vartype`, `writetable`

**Set Operations:** `innerjoin`, `outerjoin`

**Arithmetic:** `tensorprod`

**Random Number Generation:** `randstream`

**Interpolation:** `griddedinterpolant`, `scatteredinterpolant`

**Dates and Time:** `dateshift`

**Sparse Matrices:** `amd`, `bicg`, `bicgstab`, `bicgstabl`, `cgs`, `colamd`, `dissect`, `dmperm`, `eigs`, `equilibrate`, `etree`, `etreeplot`, `full`, `gmres`, `gplot`, `ichol`, `ilu`, `lsqr`, `minres`, `nzmax`, `pcg`, `qmr`, `spalloc`, `sparse`, `spaugment`, `spconvert`, `spdiags`, `speye`, `spfun`, `spones`, `spparms`, `sprand`, `sprandn`, `sprandsym`, `sprank`, `spy`, `svds`, `symamd`, `symbfact`, `symmlq`, `tfqmr`, `treelayout`, `treeplot`, `unmesh`

**Workspace:** `openvar`, `workspacebrowser`

**Error Handling (basic):** `oncleanup`

### Communications

**Modulation:** `apskdemod`, `mskdemod`, `amdemod`, `fmdemod`, `pmdemod`, `ssbdemod`

**Sources, Sinks, and Signal Operations:** `zadoffChuSeq`, `mask2shift`, `shift2mask`, `hex2poly`, `oct2poly`, `oct2dec`, `vec2mat`

**Source Coding:** `arithdeco`, `dpcmdeco`, `huffmandeco`

**Error Detection and Correction:** `crcGenerate`, `crcDetect`, `gfweight`, `syndtable`, `bchenc`, `bchdec`, `bchgenpoly`, `bchnumerr`, `rsenc`, `rsdec`, `rsgenpoly`, `rsgenpolycoeffs`, `ldpcEncode`, `ldpcDecode`, `ldpcPCM`, `ldpcQuasiCyclicMatrix`, `tpcenc`, `tpcdec`, `convenc`, `vitdec`

**Trellis and Galois Field Utilities:** `distspec`, `iscatastrophic`, `cosets`, `isprimitive`, `minpol`, `primpoly`, `gfadd`, `gfconv`, `gfcosets`, `gfdeconv`, `gfdiv`, `gffilter`, `gflineq`, `gfminpol`, `gfmul`, `gfpretty`, `gfprimck`, `gfprimdf`, `gftuple`

**Interleaving:** `intrlv`, `deintrlv`, `algintrlv`, `algdeintrlv`, `helscanintrlv`, `helscandeintrlv`, `matintrlv`, `matdeintrlv`, `randintrlv`, `randdeintrlv`, `convintrlv`, `convdeintrlv`, `helintrlv`, `heldeintrlv`, `muxintrlv`, `muxdeintrlv`

**Pulse Shaping, Equalization, MIMO:** `mlseeq`, `ofdmEqualize`, `blkdiagbfweights`, `ofdmPrecode`

**RF and Channel Impairments:** `stdchan`, `frequencyOffset`, `iqimbal`, `iqcoef2imbal`, `iqimbal2coef`, `srmdelay`, `channelDelay`, `ofdmChannelResponse`

**Propagation Path Loss and Geometry:** `fspl`, `cranerainpl`, `rainpl`, `gaspl`, `fogpl`, `raypl`, `buildingMaterialPermittivity`, `earthSurfacePermittivity`, `los`, `doppler`, `rangeangle`, `global2localcoord`, `local2globalcoord`, `cart2sphvec`, `sph2cartvec`

**Performance Analysis:** `bercoding`, `berfading`, `berfit`, `bersync`, `semianalytic`

### Control

**LTI Models:** `dss`, `pid`, `pid2`, `pidstd`, `pidstd2`, `rss`, `drss`, `dssdata`, `piddata`, `pidstddata`

**Model Conversion & Reduction:** `c2dOptions`, `d2cOptions`, `d2d`, `d2dOptions`, `canon`, `balreal`, `prescale`, `modalreal`, `compreal`, `minreal`, `sminreal`, `balred`, `modred`, `hsvd`, `pade`

**Interconnections:** `connect`, `lft`, `sumblk`

**Time and Frequency Response:** `initial`, `lsiminfo`, `gensig`, `covar`, `bodemag`, `nichols`, `sigma`, `getPeakGain`, `getGainCrossover`

**Stability and Margins:** `allmargin`

**State-Space Design and Estimation:** `lqr`, `lqry`, `lqi`, `dlqr`, `lqrd`, `lqg`, `lqgreg`, `lqgtrack`, `estim`, `kalman`, `kalmd`, `reg`, `gram`, `ctrbf`, `obsvf`

**Matrix Equations:** `lyapchol`, `dlyapchol`, `care`, `dare`, `gcare`, `gdare`

**PID Tuning and Modal Analysis:** `pidtune`, `pidtuneOptions`, `getPIDLoopResponse`, `modalsep`, `stabsep`, `freqsep`, `spectralfact`

### Fitting

**Splines:** `bspline`, `csape`, `csaps`, `cscvn`, `rscvn`, `spapi`, `spaps`, `spap2`, `spcrv`, `tpaps`, `rpmak`, `rsmak`, `spmak`, `stmak`, `fn2fm`, `fnchg`, `fndir`, `fnjmp`, `fnmin`, `fnplt`, `fnrfn`, `fntlr`, `fnxtr`, `fnzeros`, `bkbrk`, `slvblk`, `spcol`, `stcol`, `aptknt`, `chbpnt`, `newknt`, `optknt`, `smooth`, `quad2d`

### Graphics

**Line Plots:** `area`, `fimplicit`, `plot3`, `stackedplot`

**Polar Plots:** `compassplot`, `fpolarplot`, `polar` (legacy alias of polarplot), `polaraxes`, `polarbubblechart`, `polarhistogram`, `polarregion`, `polarscatter`, `radiusregion`, `rtickangle`, `rtickformat`, `rticklabels`, `rticks`, `thetaregion`, `thetatickformat`, `thetaticklabels`, `thetaticks`

**Contour Plots:** `clabel`, `contour3`, `contourc`, `contourslice`

**Vector Fields:** `compassplot`, `feather`, `quiver`, `quiver3`, `streamline`, `streamslice`

**Surface and Mesh Plots:** `contour3`, `fimplicit3`, `hidden`, `meshc`, `meshz`, `ribbon`, `surf2patch`, `surface`, `surfc`, `surfl`, `surfnorm`, `waterfall`

**Volume Visualization:** `contourslice`, `curl`, `divergence`, `flow`, `interpstreamspeed`, `isocaps`, `isocolors`, `isonormals`, `reducepatch`, `reducevolume`, `shrinkfaces`, `smooth3`, `stream2`, `stream3`, `streamline`, `streamparticles`, `streamribbon`, `streamslice`, `subvolume`, `volumebounds`

**Geographic Plots:** `geoaxes`, `geobasemap`, `geobubble`, `geodensityplot`, `geolimits`, `geoplot`, `geoscatter`, `geotickformat`

### Image

**Image Type Conversion:** `rgb2ind`

**Color Space Conversion:** `imapprox`

**Synthetic Images and Display:** `imshowpair`, `montage`, `immovie`

**Geometric Transformations:** `findbounds`, `fitgeotrans`, `imtransform`, `imwarp`, `makeresampler`

**Image Registration:** `cpcorr`, `imregconfig`, `imregcorr`, `imregdemons`, `imregister`, `imregmtb`, `imregtform`

**Image Filtering:** `gabor`

**Contrast Adjustment:** `decorrstretch`, `imlocalbrighten`, `localcontrast`

**ROI-Based Processing:** `inpaintCoherent`, `inpaintExemplar`, `roifill`

**Morphological Operations:** `bwskel`, `bwulterode`, `bwunpack`, `conndef`, `offsetstrel`

**Deblurring:** `deconvblind`, `deconvlucy`

**Neighborhood and Block Processing:** `blockproc`

**Image Segmentation:** `activecontour`, `bfscore`, `grabcut`, `imseggeodesic`, `imsegfmm`, `imsegisodata`, `imsegkmeans`, `imsegkmeans3`, `lazysnapping`, `superpixels`, `superpixels3`, `watershed`

**Object Analysis:** `circles2mask`, `corner`, `edge3`, `houghpeaks`, `imfindcircles`, `iradon`, `qtdecomp`, `qtgetblk`, `qtsetblk`, `radon`, `visboundaries`, `viscircles`

**Region and Image Properties:** `bwconvhull`, `bwferet`, `bwlabeln`, `bwselect3`, `imcontour`, `impixel`, `improfile`, `poly2label`, `regionprops3`

**Image Quality:** `brisque`, `niqe`, `piqe`

**Image Transforms:** `fan2para`, `fanbeam`, `ifanbeam`, `para2fan`

### IO

**Low-Level File I/O:** `openedfiles`

**Text Files (CSV / dlm / readtable):** `importdatatask`, `importtool`, `readcell`, `readtable`, `readtimetable`, `readvars`, `writecell`, `writetable`, `writetimetable`

**Spreadsheets:** `importdata`, `importdatatask`, `importtool`, `readcell`, `readtable`, `readtimetable`, `readvars`, `sheetnames`, `writecell`, `writetable`, `writetimetable`

**Workspace Save / Load:** `loadobj`, `saveobj`

**File Name Construction:** `filemarker`, `matlabdrive`, `matlabroot`, `toolboxdir`

### Linear Algebra

*(None — 100% complete)*

### ODE

**File Name Construction:** `decic`, `deval`, `ode`, `ode113`, `ode15i`, `ode15s`, `ode23s`, `ode23t`, `ode23tb`, `ode78`, `ode89`, `odeevent`, `odejacobian`, `odemassmatrix`, `odesensitivity`, `odextend`, `solveode`

### Optimization

**Local:** `optimize`

**Constrained:** `fmincon`, `fminunc`, `fseminf`, `fgoalattain`, `fminimax`, `linprog`, `intlinprog`, `quadprog`, `coneprog`, `secondordercone`, `lsqlin`, `lsqcurvefit`, `lsqnonlin`, `fsolve`, `mpsread`, `optimoptions`, `resetoptions`, `checkGradients`, `optimwarmstart`, `integerConstraint`

**Global:** `ga`, `gamultiobj`, `paretosearch`, `particleswarm`, `patternsearch`, `simulannealbnd`, `surrogateopt`, `packfcn`, `gaoptimset`, `gaoptimget`, `psoptimset`, `psoptimget`, `saoptimset`, `saoptimget`

### Signal

**Waveform Generation:** `buffer`, `demod`, `framelbl`, `framesig`, `modulate`, `shiftdata`, `udecode`, `uencode`, `unshiftdata`, `vco`

**Filter Design:** `cfirpm`, `designfilt`, `designfilter`, `digitalfilter`, `dspfwiz`, `filt2block`, `filteranalyzer`, `fircls`, `fircls1`, `info`, `isdouble`, `maxflat`, `polyscale`, `polystab`, `scalefiltersections`, `yulewalk`

**Digital Filter Analysis:** `filteranalyzer`, `zplane`

**Digital Filtering:** `cell2sos`, `ctf2zp`, `ctffilt`, `dspfwiz`, `eqtflength`, `filt2block`, `filtic`, `latc2tf`, `latcfilt`, `scalefiltersections`, `sos2cell`, `sos2ctf`, `tf2latc`, `zp2ctf`

**Multirate Signal Processing:** `fillgaps`

**Signal Modeling:** `stmcb`

**Correlation and Convolution:** `dtw`, `edr`, `findsignal`

**Transforms:** `digitrevorder`, `dlistft`, `dlstft`, `emd`, `fsst`, `hht`, `ifsst`, `istftlayer`, `pspectrum`, `stftlayer`, `stftmag2sig`, `vmd`, `wvd`, `xspectrogram`, `xwvd`, `fftw`, `nufft`, `nufftn`

**Windows:** `dpss`, `dpssclear`, `dpssdir`, `dpssload`, `dpsssave`, `wvtool`

**Parametric Spectral Estimation:** `pcov`, `pmcov`

**Nonparametric Spectral Estimation:** `plomb`, `pmtm`, `poctave`, `pspectrum`, `refinepeaks`

**Spectral Measurements:** `toi`

**Time-Frequency Analysis:** `dlistft`, `dlstft`, `emd`, `fsst`, `hht`, `ifsst`, `istftlayer`, `kurtogram`, `pspectrum`, `stftlayer`, `stftmag2sig`, `tfridge`, `vmd`, `wvd`, `xspectrogram`, `xwvd`

**Signal Descriptive Statistics:** `binmask2sigroi`, `countlabels`, `dtw`, `edr`, `extendsigroi`, `extractsigroi`, `filenames2labels`, `findchangepts`, `findsignal`, `folders2labels`, `framelbl`, `framesig`, `mergesigroi`, `removesigroi`, `seqperiod`, `shortensigroi`, `sigrangebinmask`, `sigroi2binmask`, `splitlabels`, `zerocrossrate`

**Vibration Analysis:** `modalfit`, `modalfrf`, `modalsd`, `orderspectrum`, `ordertrack`, `orderwaveform`, `rpmfreqmap`, `rpmordermap`, `rpmtrack`

### Audio

**Audio Feature Extraction:** `pitchnn`

### Statistics

**Descriptive Statistics:** `summary`

**Distribution Fitting (MLE / likelihood):** `mlecov`

**Multivariate Distributions:** `copulafit`, `copulaparam`, `copulastat`, `copularnd`

**Pearson / Johnson Distributions:** `pearspdf`, `pearscdf`, `pearsinv`, `pearsrnd`, `johnsrnd`

**Empirical / Kernel Distributions:** `mvksdensity`

**Hypothesis Tests:** `barttest`, `friedman`, `knntest`, `meanEffectSize`, `mmdtest`, `sampsizepwr`

**Resampling Techniques:** `cvpartition`

**Quasirandom Sequences and MCMC:** `mhsample`, `qrandstream`, `slicesample`, `sobolset`, `qrand`

**ANOVA / MANOVA / Correlation:** `anovan`, `manova1`, `aoctool`, `mauchly`, `epsilon`

**Linear Regression (function-form):** `stepwisefit`, `mvregress`, `mvregresslike`, `plsregress`, `polyconf`

**Nonlinear Regression (function-form):** `statset`, `statget`

**Hierarchical Clustering:** `dendrogram`, `optimalleaforder`

**Partitional Clustering:** `spectralcluster`

**Cluster Evaluation:** `evalclusters`, `manovacluster`

**Nearest Neighbors (function-form):** `createns`

**Hidden Markov Models:** `hmmdecode`, `hmmestimate`, `hmmgenerate`, `hmmtrain`, `hmmviterbi`

**Dimensionality Reduction:** `ppca`, `factoran`, `rica`, `sparsefilt`, `tsne`

**Feature Selection (function-form):** `fscchi2`, `fscmrmr`, `fscnca`, `fsrftest`, `fsrmrmr`, `fsrnca`, `fsulaplacian`, `relieff`, `sequentialfs`

### Wavelet

**Continuous Wavelet Transforms:** `cwt`, `icwt`, `cwtfreqbounds`, `centfrq`, `scal2frq`, `wcoherence`, `wsst`, `iwsst`, `wsstridge`, `wtmm`, `wavefun`, `wavefun2`, `wavsupport`, `qfactor`, `wavemngr`, `waveinfo`

**Discrete Wavelet Transforms (1-D):** `dwtmode`, `dwpt`, `idwpt`

**Discrete Wavelet Transforms (2-D / 3-D):** `wavedec2`, `waverec2`, `appcoef2`, `detcoef2`, `wrcoef2`, `wpdec2`, `wprec2`, `haart2`, `ihaart2`, `wavedec3`, `waverec3`, `dwt3`, `idwt3`

**Stationary, MODWT, and Wavelet Packets:** `swt2`, `iswt2`, `modwtmra`, `modwtcorr`, `modwtvar`, `modwtxcorr`, `modwpt`, `imodwpt`, `wpdec`, `wprec`, `wpcoef`, `wprcoef`, `besttree`

**Denoising and Compression:** `wdenoise2`, `wden`, `wdencmp`, `wpdencmp`, `wvarchg`, `ddencmp`, `thselect`, `wthcoef`, `wthcoef2`, `wmulden`, `measerr`, `wnoise`, `wcompress`

**Filter Banks and Wavelet Families:** `biorfilt`, `dbaux`, `symaux`, `biorwavf`, `rbiowavf`, `fejerkorovkin`, `mbscalf`, `hanscalf`, `blscalf`, `bswfun`, `isbiorthwfb`, `isorthwfb`, `wavelets`, `waveletfamilies`, `wavenames`

**Continuous Wavelet Shapes:** `meyer`, `intwave`, `pat2cwav`

**Lifting:** `lwt`, `ilwt`, `lwt2`, `ilwt2`, `lwtcoef`, `lwtcoef2`

**Decomposition Trees and Misc:** `dualtree`, `idualtree`, `dualtree2`, `idualtree2`, `dddtree`, `idddtree`, `tqwt`, `itqwt`, `wfbm`, `wfbmesti`, `wfusimg`, `wfusmat`, `wentropy`
