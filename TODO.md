# TODO

### to fix:
1. risolvi problema legato alla necessità di duplicare gli oggetti in API deployata con flag 'workers' > 1.
2. esponi modelli di embeddings e vector soters come servizi API capaci di implementare parallelismo mantenendo efficiente il sistema.
3. quando un oggetto viene caricato in memoria da un worker, tale informazione è scritta su di un registro di log (file json), in tal modo prima di tentare il l'impiego dell'oggetto gi altri workers possono verificare se vi è necessità di 'sincronizzazione' 