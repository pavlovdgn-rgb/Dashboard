# Foundation (scan)

**Источник:** [Elastic UI, Components](https://www.figma.com/design/SNBSKtwsO81j3BdjRGFpAw/Elastic-UI--Copy-?node-id=23678-450). **Дата:** 2026-09-21.
**Статус: полный.** Значения получены для 273 из 273 переменных.

**Цветовое направление продукта выбрано по референсу.** Предложенные значения — в [product-palette.md](product-palette.md). Ниже точный индекс исходной библиотеки; её значения не заменены палитрой продукта.

## Фактическая организация

В файле три коллекции: Color mode, Dimensions, Typographic scale. Отдельные Primitive/Semantic/Component коллекции не обнаружены. В прочитанной части есть прямые значения и alias внутри общей структуры; не выдаём её за трёхслойную архитектуру. Разделить уровни можно предложить на этапе адаптации, но сейчас ничего не перестраивается.

## Color mode

Коллекция `VariableCollectionId:37389:395860`. Прочитано 231 / 231. Режим по умолчанию: Light.

| Имя / Variable ID | Тип | Light | Dark |
| --- | --- | --- | --- |
| Visualization Palettes/Color Blind/Text/☠️ Color 6<br>`VariableID:38090:395915` | COLOR | #756A56 | #B9A888 |
| Visualization Palettes/Color Blind/Text/☠️ Color 7<br>`VariableID:38090:395916` | COLOR | #915C2E | #DA8B45 |
| Visualization Palettes/Color Blind/Text/☠️ Color 8<br>`VariableID:38090:395917` | COLOR | #92564A | #BA8275 |
| Button/Group/Borders/☠️ Selected<br>`VariableID:38581:395576` | COLOR | #FFFFFF; α=0.2 | #1D1E24; α=0.2 |
| Tree View/☠️ Hover + Focus<br>`VariableID:40127:404087` | COLOR | #343741; α=0.1 | #DFE5EF; α=0.2 |
| Badge/Backgrounds/☠️ Disabled<br>`VariableID:40484:40773` | COLOR | → Button/Filled/Backgrounds/☠️ Disabled (`VariableID:38564:395541`) | → Button/Filled/Backgrounds/☠️ Disabled (`VariableID:38564:395541`) |
| Badge/Text/☠️ Hollow<br>`VariableID:40484:40778` | COLOR | → Special/☠️ Ink (`VariableID:37662:395931`) | → Special/☠️ Ghost (`VariableID:37662:395932`) |
| Badge/Text/☠️ Accent<br>`VariableID:40484:40780` | COLOR | → Button/Filled/Text/☠️ Accent (`VariableID:38576:395550`) | → Button/Filled/Text/☠️ Accent (`VariableID:38576:395550`) |
| Badge/Text/☠️ Success<br>`VariableID:40484:40781` | COLOR | → Button/Filled/Text/☠️ Success (`VariableID:38576:395551`) | → Button/Filled/Text/☠️ Success (`VariableID:38576:395551`) |
| Badge/Text/☠️ Danger<br>`VariableID:40484:40783` | COLOR | → Button/Filled/Text/☠️ Danger (`VariableID:38576:395553`) | → Button/Filled/Text/☠️ Danger (`VariableID:38576:395553`) |
| Badge/Text/☠️ Accent (Alternative)<br>`VariableID:40484:40789` | COLOR | → Special/☠️ Ghost (`VariableID:37662:395932`) | → Special/☠️ Ink (`VariableID:37662:395931`) |
| Badge/Text/☠️ Subdued<br>`VariableID:40484:40790` | COLOR | → Special/☠️ Ink (`VariableID:37662:395931`) | → Special/☠️ Ghost (`VariableID:37662:395932`) |
| Comment List/Backgrounds/☠️ Neutral<br>`VariableID:43196:311975` | COLOR | → Shades/☠️ Light (`VariableID:37638:395902`) | → Shades/☠️ Light (`VariableID:37638:395902`) |
| Comment List/Backgrounds/☠️ Subdued<br>`VariableID:43196:311976` | COLOR | #E0E5EE | #71737A |
| Comment List/Backgrounds/☠️ Disabled<br>`VariableID:43196:311977` | COLOR | → Button/Filled/Backgrounds/☠️ Disabled (`VariableID:38564:395541`) | → Button/Filled/Backgrounds/☠️ Disabled (`VariableID:38564:395541`) |
| Comment List/Backgrounds/☠️ Hollow<br>`VariableID:43196:311978` | COLOR | → Shades/☠️ Empty (`VariableID:37638:395900`) | → Shades/☠️ Empty (`VariableID:37638:395900`) |
| Comment List/Backgrounds/☠️ Primary<br>`VariableID:43196:311979` | COLOR | → Button/Filled/Backgrounds/☠️ Primary (`VariableID:38564:395534`) | → Button/Filled/Backgrounds/☠️ Primary (`VariableID:38564:395534`) |
| Comment List/Backgrounds/☠️ Success<br>`VariableID:43196:311980` | COLOR | → Button/Filled/Backgrounds/☠️ Success (`VariableID:38564:395535`) | → Button/Filled/Backgrounds/☠️ Success (`VariableID:38564:395535`) |
| Comment List/Backgrounds/☠️ Warning<br>`VariableID:43196:311981` | COLOR | → Button/Filled/Backgrounds/☠️ Warning (`VariableID:38564:395536`) | → Button/Filled/Backgrounds/☠️ Warning (`VariableID:38564:395536`) |
| Comment List/Backgrounds/☠️ Danger<br>`VariableID:43196:311982` | COLOR | → Button/Filled/Backgrounds/☠️ Danger (`VariableID:38564:395537`) | → Button/Filled/Backgrounds/☠️ Danger (`VariableID:38564:395537`) |
| Comment List/Backgrounds/☠️ Accent<br>`VariableID:43196:311983` | COLOR | → Button/Filled/Backgrounds/☠️ Accent (`VariableID:38564:395539`) | → Button/Filled/Backgrounds/☠️ Accent (`VariableID:38564:395539`) |
| Comment List/Backgrounds/☠️ Accent (Alternative)<br>`VariableID:43196:311984` | COLOR | → Text/☠️ Accent (`VariableID:37641:395919`) | → Text/☠️ Accent (`VariableID:37641:395919`) |
| Comment List/Borders/☠️ Hollow<br>`VariableID:43196:311985` | COLOR | → Shades/☠️ Light (`VariableID:37638:395902`) | #52555E |
| Comment List/Text/☠️ Neutral<br>`VariableID:43196:311986` | COLOR | → Special/☠️ Ink (`VariableID:37662:395931`) | → Special/☠️ Ghost (`VariableID:37662:395932`) |
| Comment List/Text/☠️ Subdued<br>`VariableID:43196:311987` | COLOR | → Special/☠️ Ink (`VariableID:37662:395931`) | → Special/☠️ Ghost (`VariableID:37662:395932`) |
| Comment List/Text/☠️ Disabled<br>`VariableID:43196:311988` | COLOR | → Button/Filled/Text/☠️ Disabled (`VariableID:38576:395555`) | → Button/Filled/Text/☠️ Disabled (`VariableID:38576:395555`) |
| Comment List/Text/☠️ Hollow<br>`VariableID:43196:311989` | COLOR | → Special/☠️ Ink (`VariableID:37662:395931`) | → Special/☠️ Ghost (`VariableID:37662:395932`) |
| Comment List/Text/☠️ Primary<br>`VariableID:43196:311990` | COLOR | → Button/Filled/Text/☠️ Primary (`VariableID:38576:395549`) | → Button/Filled/Text/☠️ Primary (`VariableID:38576:395549`) |
| Comment List/Text/☠️ Success<br>`VariableID:43196:311991` | COLOR | → Button/Filled/Text/☠️ Success (`VariableID:38576:395551`) | → Button/Filled/Text/☠️ Success (`VariableID:38576:395551`) |
| Comment List/Text/☠️ Warning<br>`VariableID:43196:311992` | COLOR | → Button/Filled/Text/☠️ Warning (`VariableID:38576:395552`) | → Button/Filled/Text/☠️ Warning (`VariableID:38576:395552`) |
| Comment List/Text/☠️ Danger<br>`VariableID:43196:311993` | COLOR | → Button/Filled/Text/☠️ Danger (`VariableID:38576:395553`) | → Button/Filled/Text/☠️ Danger (`VariableID:38576:395553`) |
| Comment List/Text/☠️ Accent<br>`VariableID:43196:311994` | COLOR | → Button/Filled/Text/☠️ Accent (`VariableID:38576:395550`) | → Button/Filled/Text/☠️ Accent (`VariableID:38576:395550`) |
| Comment List/Text/☠️ Accent (Alternative)<br>`VariableID:43196:311995` | COLOR | → Special/☠️ Ghost (`VariableID:37662:395932`) | → Special/☠️ Ink (`VariableID:37662:395931`) |
| Button/Default/Backgrounds/☠️ Text<br>`VariableID:43559:3360` | COLOR | #E1E2E5 | #2A2C34 |
| Shades/☠️ Empty<br>`VariableID:37638:395900` | COLOR | → Plain/Light [внешняя] (`VariableID:ba65a7c5d7794d67a239ce8106a0d845baf75bda/9050:2663`) | → Shades/145 [внешняя] (`VariableID:23baad0b0275e1a3e243ad43cc53f754f72d2d9d/9057:168`) |
| Shades/☠️ Lightest<br>`VariableID:37638:395901` | COLOR | → Shades/10 [внешняя] (`VariableID:0a229da56861dc2aa851b9cab8694aad4a5dafe9/9057:119`) | → Plain/Dark [внешняя] (`VariableID:9e1494ba084245dad55810ebde635a36d72765bf/9050:2671`) |
| Shades/☠️ Light<br>`VariableID:37638:395902` | COLOR | → Shades/20 [внешняя] (`VariableID:86623ddeef09b983254b4d9e7b6eb6534f87151c/9057:164`) | → Shades/120 [внешняя] (`VariableID:da64ee1fa24f067a5d6a5fd3b2153d1ce280d74d/9057:165`) |
| Shades/☠️ Medium<br>`VariableID:37638:395903` | COLOR | → Shades/60 [внешняя] (`VariableID:2b37c2ffc9be925275ee5264486501323fd0af15/9057:121`) | → Shades/95 [внешняя] (`VariableID:d6fe1597528773b0aa503c141b685f3886a52670/9057:137`) |
| Shades/☠️ Dark<br>`VariableID:37638:395904` | COLOR | → Shades/90 [внешняя] (`VariableID:fdee217e7916ece5bb2a2e74333b71d32a12e2ff/9057:86`) | → Shades/75 [внешняя] (`VariableID:3b7ad9dd56b70632e0b66625104ad2a2fe51b4d5/9057:99`) |
| Shades/☠️ Darkest<br>`VariableID:37638:395905` | COLOR | → Shades/120 [внешняя] (`VariableID:da64ee1fa24f067a5d6a5fd3b2153d1ce280d74d/9057:165`) | → Shades/30 [внешняя] (`VariableID:e95997b50ac5a14eb10a05cac2eafab3d6cb4c8c/9057:124`) |
| Shades/☠️ Full<br>`VariableID:37638:395906` | COLOR | → Plain/Dark [внешняя] (`VariableID:9e1494ba084245dad55810ebde635a36d72765bf/9050:2671`) | → Plain/Light [внешняя] (`VariableID:ba65a7c5d7794d67a239ce8106a0d845baf75bda/9050:2663`) |
| Brand/☠️ Primary<br>`VariableID:37638:395907` | COLOR | → Primary/90 [внешняя] (`VariableID:897bc023ab76b19c377c0f62222f953bb8bc69d1/9072:29`) | → Primary/60 [внешняя] (`VariableID:d59171c5c788b201412120e5fdb359279f6fab11/9072:5`) |
| Brand/☠️ Accent<br>`VariableID:37638:395908` | COLOR | → Accent/90 [внешняя] (`VariableID:63b0028c042e0e5b4d908aaab553fe2fd40fc52d/9050:2054`) | → Accent/60 [внешняя] (`VariableID:9f0277f877ae2997671d0299a792e857b789e1c4/9050:2128`) |
| Brand/☠️ Success<br>`VariableID:37638:395909` | COLOR | → Success/90 [внешняя] (`VariableID:af3dfc0c32a62618b4b4af46417729b652bb2d61/9050:2088`) | → Success/60 [внешняя] (`VariableID:6406b6122d0d48fcf913522f013cfec7a1884d96/9050:2087`) |
| Brand/☠️ Warning<br>`VariableID:37638:395910` | COLOR | → Warning/40 [внешняя] (`VariableID:8448f92e96afedc4d6dcb359cb231267b9c02bd4/9050:2112`) | → Warning/40 [внешняя] (`VariableID:8448f92e96afedc4d6dcb359cb231267b9c02bd4/9050:2112`) |
| Brand/☠️ Danger<br>`VariableID:37638:395911` | COLOR | → Danger/90 [внешняя] (`VariableID:69fb1adaf24650dca9d65e08ee1923c1d04ed21a/9050:2132`) | → Danger/60 [внешняя] (`VariableID:eec170fb1839db30c0de40a7b8d8ff3184cce44f/9050:2268`) |
| Text/☠️ Default<br>`VariableID:37638:395912` | COLOR | → Shades/130 [внешняя] (`VariableID:de3dbb603d7227e4043a4b5a3e6193175fe652cf/9057:155`) | → Shades/30 [внешняя] (`VariableID:e95997b50ac5a14eb10a05cac2eafab3d6cb4c8c/9057:124`) |
| Text/☠️ Subdued<br>`VariableID:37641:395913` | COLOR | → Shades/95 [внешняя] (`VariableID:d6fe1597528773b0aa503c141b685f3886a52670/9057:137`) | → Shades/60 [внешняя] (`VariableID:2b37c2ffc9be925275ee5264486501323fd0af15/9057:121`) |
| Text/☠️ Title<br>`VariableID:37641:395914` | COLOR | → Shades/140 [внешняя] (`VariableID:0681f10656d2e405d89832ad207f9df579765628/9057:156`) | → Shades/20 [внешняя] (`VariableID:86623ddeef09b983254b4d9e7b6eb6534f87151c/9057:164`) |
| Text/☠️ Disabled<br>`VariableID:37641:395915` | COLOR | → Shades/80 [внешняя] (`VariableID:e9839fe05d43b59074ccc67dd353da7bfb989749/9057:89`) | → Shades/80 [внешняя] (`VariableID:e9839fe05d43b59074ccc67dd353da7bfb989749/9057:89`) |
| Text/☠️ Primary<br>`VariableID:37641:395916` | COLOR | → Primary/100 [внешняя] (`VariableID:cb7f698376a1a88df6534ff96b4f81a8e13b0f5f/9072:36`) | → Primary/60 [внешняя] (`VariableID:d59171c5c788b201412120e5fdb359279f6fab11/9072:5`) |
| Text/☠️ Success<br>`VariableID:37641:395918` | COLOR | → Success/100 [внешняя] (`VariableID:e97579d2c349f271c51711c5f5720d110cc3a768/9050:2073`) | → Success/60 [внешняя] (`VariableID:6406b6122d0d48fcf913522f013cfec7a1884d96/9050:2087`) |
| Text/☠️ Accent<br>`VariableID:37641:395919` | COLOR | → Accent/100 [внешняя] (`VariableID:e6e4f29733ea77d852bfebaa79437c7b374708e7/9050:2039`) | → Accent/60 [внешняя] (`VariableID:9f0277f877ae2997671d0299a792e857b789e1c4/9050:2128`) |
| Text/☠️ Warning<br>`VariableID:37641:395920` | COLOR | → Warning/110 [внешняя] (`VariableID:022ce01c80006aa6dec39850fe9a9690afc5778b/9050:2100`) | → Warning/30 [внешняя] (`VariableID:c4a62faf5a8da618f28058c5753cb8f08d985acb/9050:2115`) |
| Text/☠️ Danger<br>`VariableID:37641:395921` | COLOR | → Danger/100 [внешняя] (`VariableID:e6688bf7de16eeb860171950b47cce756a3b0117/9050:2199`) | → Danger/60 [внешняя] (`VariableID:eec170fb1839db30c0de40a7b8d8ff3184cce44f/9050:2268`) |
| Backgrounds/Opaque/☠️ Plain<br>`VariableID:37641:395922` | COLOR | → Plain/Light [внешняя] (`VariableID:ba65a7c5d7794d67a239ce8106a0d845baf75bda/9050:2663`) | → Shades/145 [внешняя] (`VariableID:23baad0b0275e1a3e243ad43cc53f754f72d2d9d/9057:168`) |
| Special/☠️ Body (AKA Page)<br>`VariableID:37641:395923` | COLOR | → Shades/10 [внешняя] (`VariableID:0a229da56861dc2aa851b9cab8694aad4a5dafe9/9057:119`) | → Plain/Dark [внешняя] (`VariableID:9e1494ba084245dad55810ebde635a36d72765bf/9050:2671`) |
| Backgrounds/Opaque/☠️ Primary<br>`VariableID:37641:395924` | COLOR | → Primary/10 [внешняя] (`VariableID:f1e3e5660bd932f16a620d7a8c5e2b24699a202f/9072:38`) | → Primary/140 [внешняя] (`VariableID:bfc00188dbf5fe4bbb39600906cca3a0818091cd/9072:18`) |
| Backgrounds/Opaque/☠️ Success<br>`VariableID:37641:395925` | COLOR | → Success/10 [внешняя] (`VariableID:83e3304a9059e062d88f9f0ea358303dd92b512f/9050:2200`) | → Success/140 [внешняя] (`VariableID:685b07a509a58631bfed1fa9c7e67690a9d55a90/9050:2156`) |
| Backgrounds/Opaque/☠️ Warning<br>`VariableID:37641:395926` | COLOR | → Warning/10 [внешняя] (`VariableID:f5e056614de9e03bc8ebb28861ec4982b6a05f3a/9050:2193`) | → Warning/140 [внешняя] (`VariableID:3f489f5278613d77464bee53b3a5357518d38216/9050:2246`) |
| Backgrounds/Opaque/☠️ Danger<br>`VariableID:37641:395927` | COLOR | → Danger/10 [внешняя] (`VariableID:3b574dfecbe1845c84d31b53c8a84b66ff45b94d/9050:2264`) | → Danger/140 [внешняя] (`VariableID:c92170cf1b24a68e2ff271f5c7afabbf04a14084/9050:2085`) |
| Backgrounds/Opaque/☠️ Accent<br>`VariableID:37641:395928` | COLOR | → Accent/10 [внешняя] (`VariableID:1bc8b2939940b72180f06b1fa0e73d1975ce068d/9050:2068`) | → Accent/140 [внешняя] (`VariableID:bebfec47702f638e6455e660abedc8f537460e70/9050:2052`) |
| Special/☠️ Ink<br>`VariableID:37662:395931` | COLOR | → Plain/Dark [внешняя] (`VariableID:9e1494ba084245dad55810ebde635a36d72765bf/9050:2671`) | → Plain/Dark [внешняя] (`VariableID:9e1494ba084245dad55810ebde635a36d72765bf/9050:2671`) |
| Special/☠️ Ghost<br>`VariableID:37662:395932` | COLOR | → Plain/Light [внешняя] (`VariableID:ba65a7c5d7794d67a239ce8106a0d845baf75bda/9050:2663`) | → Plain/Light [внешняя] (`VariableID:ba65a7c5d7794d67a239ce8106a0d845baf75bda/9050:2663`) |
| Special/☠️ Disabled<br>`VariableID:37662:395933` | COLOR | → Shades/15 [внешняя] (`VariableID:ef329b3dd8c11d09fc98790367af207169238791/9057:132`) | → Shades/130 [внешняя] (`VariableID:de3dbb603d7227e4043a4b5a3e6193175fe652cf/9057:155`) |
| Special/☠️ Shadow<br>`VariableID:37662:395934` | COLOR | → Special/☠️ Ink (`VariableID:37662:395931`) | → Special/☠️ Ink (`VariableID:37662:395931`) |
| Backgrounds/Opaque/☠️ Subdued<br>`VariableID:37667:395940` | COLOR | → Special/☠️ Body (AKA Page) (`VariableID:37641:395923`) | → Special/☠️ Body (AKA Page) (`VariableID:37641:395923`) |
| Text/☠️ Link<br>`VariableID:37667:395944` | COLOR | → Text/☠️ Primary (`VariableID:37641:395916`) | → Text/☠️ Primary (`VariableID:37641:395916`) |
| Special/☠️ Select<br>`VariableID:37667:395947` | COLOR | → Primary/10 [внешняя] (`VariableID:f1e3e5660bd932f16a620d7a8c5e2b24699a202f/9072:38`) | → Primary/130 [внешняя] (`VariableID:c866effb8f1ef18c58aee0f8d876c41e9d632474/9072:31`) |
| Visualization palettes/Color blind/Text/☠️ Color 0<br>`VariableID:38090:395909` | COLOR | → Accent secondary/100 [внешняя] (`VariableID:01c160dd2e80ebd3ff5aee871af44af1d5805737/9050:2060`) | → Accent secondary/60 [внешняя] (`VariableID:df6e6471181c634a3d7e3fe6763be3ccbc9511d2/9050:2093`) |
| Visualization palettes/Color blind/Text/☠️ Color 1<br>`VariableID:38090:395910` | COLOR | → Primary/100 [внешняя] (`VariableID:cb7f698376a1a88df6534ff96b4f81a8e13b0f5f/9072:36`) | → Primary/60 [внешняя] (`VariableID:d59171c5c788b201412120e5fdb359279f6fab11/9072:5`) |
| Visualization palettes/Color blind/Text/☠️ Color 2<br>`VariableID:38090:395911` | COLOR | → Accent/100 [внешняя] (`VariableID:e6e4f29733ea77d852bfebaa79437c7b374708e7/9050:2039`) | → Accent/60 [внешняя] (`VariableID:9f0277f877ae2997671d0299a792e857b789e1c4/9050:2128`) |
| Visualization palettes/Color blind/Text/☠️ Color 6<br>`VariableID:38090:395912` | COLOR | → Assistance/100 [внешняя] (`VariableID:1f5fb8c96abe09ed8ec23e7596ad45b67b616b5c/9050:2078`) | → Assistance/60 [внешняя] (`VariableID:955e13e7472d3030fdd19cff4d1b062084f29019/9050:2183`) |
| Visualization palettes/Color blind/Text/☠️ Color 5<br>`VariableID:38090:395913` | COLOR | → Success/100 [внешняя] (`VariableID:e97579d2c349f271c51711c5f5720d110cc3a768/9050:2073`) | → Success/60 [внешняя] (`VariableID:6406b6122d0d48fcf913522f013cfec7a1884d96/9050:2087`) |
| Visualization palettes/Color blind/Text/☠️ Color 4<br>`VariableID:38090:395914` | COLOR | → Warning/100 [внешняя] (`VariableID:81fcc6ff9eaabb71102d3b83d974d8faf2a2cd5c/9050:2139`) | → Warning/60 [внешняя] (`VariableID:93e9b8d2cb36b89054978e06701c4ffcadd22370/9050:2242`) |
| Visualization palettes/Color blind/Text/☠️ Color 3<br>`VariableID:38090:395918` | COLOR | → Danger/100 [внешняя] (`VariableID:e6688bf7de16eeb860171950b47cce756a3b0117/9050:2199`) | → Danger/60 [внешняя] (`VariableID:eec170fb1839db30c0de40a7b8d8ff3184cce44f/9050:2268`) |
| Button/Default/Backgrounds/☠️ Primary<br>`VariableID:38562:395518` | COLOR | → Primary/20 [внешняя] (`VariableID:52c828cdeab229bc5d3668b125b8ac25f75c7da8/9072:9`) | → Primary/130 [внешняя] (`VariableID:c866effb8f1ef18c58aee0f8d876c41e9d632474/9072:31`) |
| Button/Default/Backgrounds/☠️ Success<br>`VariableID:38562:395519` | COLOR | → Success/20 [внешняя] (`VariableID:dcefc5c752a2429d7a9e2f45f28b8dcc8ba67c13/9050:2118`) | → Success/130 [внешняя] (`VariableID:b94e829291a6146bb544c6ccdf359cd9edf4ee62/9050:2047`) |
| Button/Default/Backgrounds/☠️ Warning<br>`VariableID:38562:395527` | COLOR | → Warning/20 [внешняя] (`VariableID:b22559cf15419e2c574486d0de0b0efe939aadf7/9050:2167`) | → Warning/130 [внешняя] (`VariableID:2637e6567676eaf0363c73661b4d874c68005b0c/9050:2216`) |
| Button/Default/Backgrounds/☠️ Danger<br>`VariableID:38562:395528` | COLOR | → Danger/20 [внешняя] (`VariableID:7679d361dae449e5fff6148218f8e042307dfc19/9050:2228`) | → Danger/130 [внешняя] (`VariableID:837f4b5e06ca626f8d92a42dd245701403ec67ca/9050:2171`) |
| Button/Default/Backgrounds/☠️ Neutral<br>`VariableID:38562:395529` | COLOR | → Shades/20 [внешняя] (`VariableID:86623ddeef09b983254b4d9e7b6eb6534f87151c/9057:164`) | → Shades/130 [внешняя] (`VariableID:de3dbb603d7227e4043a4b5a3e6193175fe652cf/9057:155`) |
| Button/Default/Backgrounds/☠️ Accent<br>`VariableID:38562:395530` | COLOR | → Accent/20 [внешняя] (`VariableID:01cdfb1a8cd763c9785c354351c74722b54707db/9050:2062`) | → Accent/130 [внешняя] (`VariableID:c5090f89158578e0217e86e52d4935eb40ebc612/9050:2205`) |
| Button/Default/Backgrounds/☠️ Disabled<br>`VariableID:38564:395531` | COLOR | → Special/☠️ Disabled (`VariableID:37662:395933`) | → Special/☠️ Disabled (`VariableID:37662:395933`) |
| Button/Filled/Backgrounds/☠️ Primary<br>`VariableID:38564:395534` | COLOR | → Brand/☠️ Primary (`VariableID:37638:395907`) | → Brand/☠️ Primary (`VariableID:37638:395907`) |
| Button/Filled/Backgrounds/☠️ Success<br>`VariableID:38564:395535` | COLOR | → Brand/☠️ Success (`VariableID:37638:395909`) | → Brand/☠️ Success (`VariableID:37638:395909`) |
| Button/Filled/Backgrounds/☠️ Warning<br>`VariableID:38564:395536` | COLOR | → Brand/☠️ Warning (`VariableID:37638:395910`) | → Brand/☠️ Warning (`VariableID:37638:395910`) |
| Button/Filled/Backgrounds/☠️ Danger<br>`VariableID:38564:395537` | COLOR | → Brand/☠️ Danger (`VariableID:37638:395911`) | → Brand/☠️ Danger (`VariableID:37638:395911`) |
| Button/Filled/Backgrounds/☠️ Neutral<br>`VariableID:38564:395538` | COLOR | → Shades/☠️ Dark (`VariableID:37638:395904`) | → Shades/☠️ Dark (`VariableID:37638:395904`) |
| Button/Filled/Backgrounds/☠️ Accent<br>`VariableID:38564:395539` | COLOR | → Brand/☠️ Accent (`VariableID:37638:395908`) | → Brand/☠️ Accent (`VariableID:37638:395908`) |
| Button/Filled/Backgrounds/☠️ Disabled<br>`VariableID:38564:395541` | COLOR | → Special/☠️ Disabled (`VariableID:37662:395933`) | → Special/☠️ Disabled (`VariableID:37662:395933`) |
| Button/Default/Text/☠️ Primary<br>`VariableID:38564:395542` | COLOR | → Text/☠️ Primary (`VariableID:37641:395916`) | → Text/☠️ Primary (`VariableID:37641:395916`) |
| Button/Default/Text/☠️ Accent<br>`VariableID:38564:395543` | COLOR | → Text/☠️ Accent (`VariableID:37641:395919`) | → Text/☠️ Accent (`VariableID:37641:395919`) |
| Button/Default/Text/☠️ Success<br>`VariableID:38564:395544` | COLOR | → Text/☠️ Success (`VariableID:37641:395918`) | → Text/☠️ Success (`VariableID:37641:395918`) |
| Button/Default/Text/☠️ Warning<br>`VariableID:38564:395545` | COLOR | → Text/☠️ Warning (`VariableID:37641:395920`) | → Text/☠️ Warning (`VariableID:37641:395920`) |
| Button/Default/Text/☠️ Danger<br>`VariableID:38564:395546` | COLOR | → Text/☠️ Danger (`VariableID:37641:395921`) | → Text/☠️ Danger (`VariableID:37641:395921`) |
| Button/Default/Text/☠️ Neutral<br>`VariableID:38564:395547` | COLOR | → Text/☠️ Default (`VariableID:37638:395912`) | → Text/☠️ Default (`VariableID:37638:395912`) |
| Button/Default/Text/☠️ Disabled<br>`VariableID:38564:395548` | COLOR | → Text/☠️ Disabled (`VariableID:37641:395915`) | → Text/☠️ Disabled (`VariableID:37641:395915`) |
| Button/Filled/Text/☠️ Primary<br>`VariableID:38576:395549` | COLOR | → Special/☠️ Ghost (`VariableID:37662:395932`) | → Special/☠️ Ink (`VariableID:37662:395931`) |
| Button/Filled/Text/☠️ Accent<br>`VariableID:38576:395550` | COLOR | → Special/☠️ Ghost (`VariableID:37662:395932`) | → Special/☠️ Ink (`VariableID:37662:395931`) |
| Button/Filled/Text/☠️ Success<br>`VariableID:38576:395551` | COLOR | → Special/☠️ Ghost (`VariableID:37662:395932`) | → Special/☠️ Ink (`VariableID:37662:395931`) |
| Button/Filled/Text/☠️ Warning<br>`VariableID:38576:395552` | COLOR | → Warning/110 [внешняя] (`VariableID:022ce01c80006aa6dec39850fe9a9690afc5778b/9050:2100`) | → Warning/110 [внешняя] (`VariableID:022ce01c80006aa6dec39850fe9a9690afc5778b/9050:2100`) |
| Button/Filled/Text/☠️ Danger<br>`VariableID:38576:395553` | COLOR | → Special/☠️ Ghost (`VariableID:37662:395932`) | → Special/☠️ Ink (`VariableID:37662:395931`) |
| Button/Filled/Text/☠️ Neutral<br>`VariableID:38576:395554` | COLOR | → Special/☠️ Ghost (`VariableID:37662:395932`) | → Special/☠️ Ink (`VariableID:37662:395931`) |
| Button/Filled/Text/☠️ Disabled<br>`VariableID:38576:395555` | COLOR | → Button/Default/Text/☠️ Disabled (`VariableID:38564:395548`) | → Button/Default/Text/☠️ Disabled (`VariableID:38564:395548`) |
| Button/Empty/Text/☠️ Primary<br>`VariableID:38581:395556` | COLOR | → Button/Default/Text/☠️ Primary (`VariableID:38564:395542`) | → Button/Default/Text/☠️ Primary (`VariableID:38564:395542`) |
| Button/Empty/Text/☠️ Accent<br>`VariableID:38581:395557` | COLOR | → Button/Default/Text/☠️ Accent (`VariableID:38564:395543`) | → Button/Default/Text/☠️ Accent (`VariableID:38564:395543`) |
| Button/Empty/Text/☠️ Success<br>`VariableID:38581:395558` | COLOR | → Button/Default/Text/☠️ Success (`VariableID:38564:395544`) | → Button/Default/Text/☠️ Success (`VariableID:38564:395544`) |
| Button/Empty/Text/☠️ Warning<br>`VariableID:38581:395559` | COLOR | → Button/Default/Text/☠️ Warning (`VariableID:38564:395545`) | → Button/Default/Text/☠️ Warning (`VariableID:38564:395545`) |
| Button/Empty/Text/☠️ Danger<br>`VariableID:38581:395560` | COLOR | → Button/Default/Text/☠️ Danger (`VariableID:38564:395546`) | → Button/Default/Text/☠️ Danger (`VariableID:38564:395546`) |
| Button/Empty/Text/☠️ Neutral<br>`VariableID:38581:395561` | COLOR | → Button/Default/Text/☠️ Neutral (`VariableID:38564:395547`) | → Button/Default/Text/☠️ Neutral (`VariableID:38564:395547`) |
| Button/Empty/Text/☠️ Disabled<br>`VariableID:38581:395562` | COLOR | → Button/Default/Text/☠️ Disabled (`VariableID:38564:395548`) | → Button/Default/Text/☠️ Disabled (`VariableID:38564:395548`) |
| Button/Group/Borders/☠️ Unselected<br>`VariableID:38581:395575` | COLOR | → Shades/30 [внешняя] (`VariableID:e95997b50ac5a14eb10a05cac2eafab3d6cb4c8c/9057:124`) | → Shades/100 [внешняя] (`VariableID:8e4d08f8cc678569aa83b938727b0f29db556bc7/9057:112`) |
| Button/Group/Backgrounds/☠️ Disabled + Selected<br>`VariableID:38581:395577` | COLOR | → Special/☠️ Disabled (`VariableID:37662:395933`) | → Special/☠️ Disabled (`VariableID:37662:395933`) |
| Button/Group/Text/☠️ Disabled + Selected<br>`VariableID:38581:395578` | COLOR | → Shades/80 [внешняя] (`VariableID:e9839fe05d43b59074ccc67dd353da7bfb989749/9057:89`) | → Shades/80 [внешняя] (`VariableID:e9839fe05d43b59074ccc67dd353da7bfb989749/9057:89`) |
| Form controls/Borders/☠️ Default<br>`VariableID:38582:395687` | COLOR | → Shades/30 [внешняя] (`VariableID:e95997b50ac5a14eb10a05cac2eafab3d6cb4c8c/9057:124`) | → Shades/100 [внешняя] (`VariableID:8e4d08f8cc678569aa83b938727b0f29db556bc7/9057:112`) |
| Form controls/Backgrounds/☠️ Default<br>`VariableID:38582:395688` | COLOR | → Shades/☠️ Empty (`VariableID:37638:395900`) | → Shades/☠️ Empty (`VariableID:37638:395900`) |
| Visualization palettes/Color blind/Default/☠️ Color 0<br>`VariableID:38878:397565` | COLOR | → Accent secondary/60 [внешняя] (`VariableID:df6e6471181c634a3d7e3fe6763be3ccbc9511d2/9050:2093`) | → Accent secondary/60 [внешняя] (`VariableID:df6e6471181c634a3d7e3fe6763be3ccbc9511d2/9050:2093`) |
| Visualization palettes/Color blind/Default/☠️ Color 1<br>`VariableID:38878:397566` | COLOR | → Accent secondary/30 [внешняя] (`VariableID:b299521032032c485ae1b1fd90024160a1d79dbc/9050:2229`) | → Accent secondary/30 [внешняя] (`VariableID:b299521032032c485ae1b1fd90024160a1d79dbc/9050:2229`) |
| Visualization palettes/Color blind/Default/☠️ Color 2<br>`VariableID:38878:397567` | COLOR | → Primary/60 [внешняя] (`VariableID:d59171c5c788b201412120e5fdb359279f6fab11/9072:5`) | → Primary/60 [внешняя] (`VariableID:d59171c5c788b201412120e5fdb359279f6fab11/9072:5`) |
| Visualization palettes/Color blind/Default/☠️ Color 3<br>`VariableID:38878:397568` | COLOR | → Primary/30 [внешняя] (`VariableID:1ddfd35edca8f9131a1591b244f2ddc602fd095c/9072:33`) | → Primary/30 [внешняя] (`VariableID:1ddfd35edca8f9131a1591b244f2ddc602fd095c/9072:33`) |
| Visualization palettes/Color blind/Default/☠️ Color 4<br>`VariableID:38878:397569` | COLOR | → Accent/60 [внешняя] (`VariableID:9f0277f877ae2997671d0299a792e857b789e1c4/9050:2128`) | → Accent/60 [внешняя] (`VariableID:9f0277f877ae2997671d0299a792e857b789e1c4/9050:2128`) |
| Visualization palettes/Color blind/Default/☠️ Color 5<br>`VariableID:38878:397570` | COLOR | → Accent/30 [внешняя] (`VariableID:d958bec0dea13e2b54f425c9646ecbfd6a575a64/9050:2135`) | → Accent/30 [внешняя] (`VariableID:d958bec0dea13e2b54f425c9646ecbfd6a575a64/9050:2135`) |
| Visualization palettes/Color blind/Default/☠️ Color 6<br>`VariableID:38878:397571` | COLOR | → Danger/60 [внешняя] (`VariableID:eec170fb1839db30c0de40a7b8d8ff3184cce44f/9050:2268`) | → Danger/60 [внешняя] (`VariableID:eec170fb1839db30c0de40a7b8d8ff3184cce44f/9050:2268`) |
| Visualization palettes/Color blind/Default/☠️ Color 7<br>`VariableID:38878:397572` | COLOR | → Danger/30 [внешняя] (`VariableID:2d2e7c9531d0d9cf24b56433e180691cee0e8b9a/9050:2198`) | → Danger/30 [внешняя] (`VariableID:2d2e7c9531d0d9cf24b56433e180691cee0e8b9a/9050:2198`) |
| Visualization palettes/Color blind/Default/☠️ Color 8<br>`VariableID:38878:397573` | COLOR | → Warning/60 [внешняя] (`VariableID:93e9b8d2cb36b89054978e06701c4ffcadd22370/9050:2242`) | → Warning/60 [внешняя] (`VariableID:93e9b8d2cb36b89054978e06701c4ffcadd22370/9050:2242`) |
| Visualization palettes/Color blind/Default/☠️ Color 9<br>`VariableID:38878:397574` | COLOR | → Warning/30 [внешняя] (`VariableID:c4a62faf5a8da618f28058c5753cb8f08d985acb/9050:2115`) | → Warning/30 [внешняя] (`VariableID:c4a62faf5a8da618f28058c5753cb8f08d985acb/9050:2115`) |
| Visualization palettes/Color blind/Behind text/☠️ Color 0<br>`VariableID:38878:397575` | COLOR | → Visualization palettes/Color blind/Default/☠️ Color 0 (`VariableID:38878:397565`) | → Visualization palettes/Color blind/Default/☠️ Color 0 (`VariableID:38878:397565`) |
| Visualization palettes/Color blind/Behind text/☠️ Color 1<br>`VariableID:38878:397576` | COLOR | → Visualization palettes/Color blind/Default/☠️ Color 1 (`VariableID:38878:397566`) | → Visualization palettes/Color blind/Default/☠️ Color 1 (`VariableID:38878:397566`) |
| Visualization palettes/Color blind/Behind text/☠️ Color 2<br>`VariableID:38878:397577` | COLOR | → Visualization palettes/Color blind/Default/☠️ Color 2 (`VariableID:38878:397567`) | → Visualization palettes/Color blind/Default/☠️ Color 2 (`VariableID:38878:397567`) |
| Visualization palettes/Color blind/Behind text/☠️ Color 3<br>`VariableID:38878:397578` | COLOR | → Visualization palettes/Color blind/Default/☠️ Color 3 (`VariableID:38878:397568`) | → Visualization palettes/Color blind/Default/☠️ Color 3 (`VariableID:38878:397568`) |
| Visualization palettes/Color blind/Behind text/☠️ Color 4<br>`VariableID:38878:397579` | COLOR | → Visualization palettes/Color blind/Default/☠️ Color 4 (`VariableID:38878:397569`) | → Visualization palettes/Color blind/Default/☠️ Color 4 (`VariableID:38878:397569`) |
| Visualization palettes/Color blind/Behind text/☠️ Color 5<br>`VariableID:38878:397580` | COLOR | → Visualization palettes/Color blind/Default/☠️ Color 5 (`VariableID:38878:397570`) | → Visualization palettes/Color blind/Default/☠️ Color 5 (`VariableID:38878:397570`) |
| Visualization palettes/Color blind/Behind text/☠️ Color 6<br>`VariableID:38878:397581` | COLOR | → Visualization palettes/Color blind/Default/☠️ Color 6 (`VariableID:38878:397571`) | → Visualization palettes/Color blind/Default/☠️ Color 6 (`VariableID:38878:397571`) |
| Visualization palettes/Color blind/Behind text/☠️ Color 7<br>`VariableID:38878:397582` | COLOR | → Visualization palettes/Color blind/Default/☠️ Color 7 (`VariableID:38878:397572`) | → Visualization palettes/Color blind/Default/☠️ Color 7 (`VariableID:38878:397572`) |
| Visualization palettes/Color blind/Behind text/☠️ Color 8<br>`VariableID:38878:397583` | COLOR | → Visualization palettes/Color blind/Default/☠️ Color 8 (`VariableID:38878:397573`) | → Visualization palettes/Color blind/Default/☠️ Color 8 (`VariableID:38878:397573`) |
| Visualization palettes/Color blind/Behind text/☠️ Color 9<br>`VariableID:38878:397584` | COLOR | → Visualization palettes/Color blind/Default/☠️ Color 9 (`VariableID:38878:397574`) | → Visualization palettes/Color blind/Default/☠️ Color 9 (`VariableID:38878:397574`) |
| Backgrounds/Transparent/☠️ Plain<br>`VariableID:40124:404061` | COLOR | → Shades/15 [внешняя] (`VariableID:ef329b3dd8c11d09fc98790367af207169238791/9057:132`) | → Shades/145 [внешняя] (`VariableID:23baad0b0275e1a3e243ad43cc53f754f72d2d9d/9057:168`) |
| Backgrounds/Transparent/☠️ Subdued<br>`VariableID:40124:404062` | COLOR | → Shades/15 [внешняя] (`VariableID:ef329b3dd8c11d09fc98790367af207169238791/9057:132`) | → Plain/Dark [внешняя] (`VariableID:9e1494ba084245dad55810ebde635a36d72765bf/9050:2671`) |
| Backgrounds/Transparent/☠️ Primary<br>`VariableID:40124:404063` | COLOR | → Backgrounds/Opaque/☠️ Primary (`VariableID:37641:395924`) | → Backgrounds/Opaque/☠️ Primary (`VariableID:37641:395924`) |
| Backgrounds/Transparent/☠️ Success<br>`VariableID:40124:404064` | COLOR | → Backgrounds/Opaque/☠️ Success (`VariableID:37641:395925`) | → Backgrounds/Opaque/☠️ Success (`VariableID:37641:395925`) |
| Backgrounds/Transparent/☠️ Warning<br>`VariableID:40124:404065` | COLOR | → Backgrounds/Opaque/☠️ Warning (`VariableID:37641:395926`) | → Backgrounds/Opaque/☠️ Warning (`VariableID:37641:395926`) |
| Backgrounds/Transparent/☠️ Danger<br>`VariableID:40124:404066` | COLOR | → Backgrounds/Opaque/☠️ Danger (`VariableID:37641:395927`) | → Backgrounds/Opaque/☠️ Danger (`VariableID:37641:395927`) |
| Backgrounds/Transparent/☠️ Accent<br>`VariableID:40124:404067` | COLOR | → Backgrounds/Opaque/☠️ Accent (`VariableID:37641:395928`) | → Backgrounds/Opaque/☠️ Accent (`VariableID:37641:395928`) |
| Tooltip/☠️ Background<br>`VariableID:40125:404078` | COLOR | → Plain/Dark [внешняя] (`VariableID:9e1494ba084245dad55810ebde635a36d72765bf/9050:2671`) | → Plain/Dark [внешняя] (`VariableID:9e1494ba084245dad55810ebde635a36d72765bf/9050:2671`) |
| Tooltip/☠️ Border<br>`VariableID:40125:404079` | COLOR | → Shades/120 [внешняя] (`VariableID:da64ee1fa24f067a5d6a5fd3b2153d1ce280d74d/9057:165`) | → Shades/120 [внешняя] (`VariableID:da64ee1fa24f067a5d6a5fd3b2153d1ce280d74d/9057:165`) |
| Special/☠️ Overlay<br>`VariableID:40125:404083` | COLOR | → Shades/100 (alpha)/70% [внешняя] (`VariableID:743479f026102fa92c90bed38ce973ac38161775/9050:2032`) | → Shades/120 (alpha)/70% [внешняя] (`VariableID:7181f88de033c3150e461657f01f52aad40c360f/9050:2043`) |
| Tables/☠️ Row Selected<br>`VariableID:40125:404085` | COLOR | → Primary/10 [внешняя] (`VariableID:f1e3e5660bd932f16a620d7a8c5e2b24699a202f/9072:38`) | → Primary/130 [внешняя] (`VariableID:c866effb8f1ef18c58aee0f8d876c41e9d632474/9072:31`) |
| Tables/☠️ Row Hover<br>`VariableID:40125:404086` | COLOR | → Primary/100 (alpha)/4% [внешняя] (`VariableID:af2481e71afdf8ca05dcf94e33f9be01443c9c31/9050:2058`) | → Plain/Light (alpha)/8% [внешняя] (`VariableID:ba7c0b2be6e8c72dbc7c88d102a4508f705379e6/9050:2672`) |
| Header/Dark/☠️ Background<br>`VariableID:40127:404088` | COLOR | → Plain/Dark [внешняя] (`VariableID:9e1494ba084245dad55810ebde635a36d72765bf/9050:2671`) | → Plain/Dark [внешняя] (`VariableID:9e1494ba084245dad55810ebde635a36d72765bf/9050:2671`) |
| Header/Dark/☠️ Border<br>`VariableID:40127:404089` | COLOR | → Shades/100 [внешняя] (`VariableID:8e4d08f8cc678569aa83b938727b0f29db556bc7/9057:112`) | → Shades/100 [внешняя] (`VariableID:8e4d08f8cc678569aa83b938727b0f29db556bc7/9057:112`) |
| Header/Default/☠️ Border<br>`VariableID:40127:404090` | COLOR | → Shades/30 [внешняя] (`VariableID:e95997b50ac5a14eb10a05cac2eafab3d6cb4c8c/9057:124`) | → Shades/100 [внешняя] (`VariableID:8e4d08f8cc678569aa83b938727b0f29db556bc7/9057:112`) |
| Form controls/Backgrounds/☠️ Disabled<br>`VariableID:40149:234966` | COLOR | → Special/☠️ Disabled (`VariableID:37662:395933`) | → Special/☠️ Disabled (`VariableID:37662:395933`) |
| Form controls/Backgrounds/☠️ Read-Only<br>`VariableID:40149:234967` | COLOR | → Shades/☠️ Empty (`VariableID:37638:395900`) | → Shades/☠️ Empty (`VariableID:37638:395900`) |
| Form controls/Backgrounds/☠️ Label<br>`VariableID:40149:234969` | COLOR | → Shades/15 [внешняя] (`VariableID:ef329b3dd8c11d09fc98790367af207169238791/9057:132`) | → Shades/130 [внешняя] (`VariableID:de3dbb603d7227e4043a4b5a3e6193175fe652cf/9057:155`) |
| Selection controls/Switch/Backgrounds/☠️ Off<br>`VariableID:40310:234970` | COLOR | → Shades/90 [внешняя] (`VariableID:fdee217e7916ece5bb2a2e74333b71d32a12e2ff/9057:86`) | → Shades/60 [внешняя] (`VariableID:2b37c2ffc9be925275ee5264486501323fd0af15/9057:121`) |
| Form controls/Backgrounds/☠️ Focus<br>`VariableID:40310:234971` | COLOR | → Shades/☠️ Empty (`VariableID:37638:395900`) | → Shades/☠️ Empty (`VariableID:37638:395900`) |
| Form controls/Borders/☠️ Custom Control<br>`VariableID:40310:234972` | COLOR | → Shades/60 [внешняя] (`VariableID:2b37c2ffc9be925275ee5264486501323fd0af15/9057:121`) | → Shades/80 [внешняя] (`VariableID:e9839fe05d43b59074ccc67dd353da7bfb989749/9057:89`) |
| Badge/Backgrounds/☠️ Subdued<br>`VariableID:40425:5721` | COLOR | → Shades/20 [внешняя] (`VariableID:86623ddeef09b983254b4d9e7b6eb6534f87151c/9057:164`) | → Shades/130 [внешняя] (`VariableID:de3dbb603d7227e4043a4b5a3e6193175fe652cf/9057:155`) |
| Badge/Borders/☠️ Hollow<br>`VariableID:40475:3143` | COLOR | → Shades/30 [внешняя] (`VariableID:e95997b50ac5a14eb10a05cac2eafab3d6cb4c8c/9057:124`) | → Shades/100 [внешняя] (`VariableID:8e4d08f8cc678569aa83b938727b0f29db556bc7/9057:112`) |
| Badge/Backgrounds/☠️ Hollow<br>`VariableID:40484:40766` | COLOR | → Plain/Light [внешняя] (`VariableID:ba65a7c5d7794d67a239ce8106a0d845baf75bda/9050:2663`) | → Plain/Dark [внешняя] (`VariableID:9e1494ba084245dad55810ebde635a36d72765bf/9050:2671`) |
| Badge/Backgrounds/☠️ Primary<br>`VariableID:40484:40767` | COLOR | → Brand/☠️ Primary (`VariableID:37638:395907`) | → Brand/☠️ Primary (`VariableID:37638:395907`) |
| Badge/Backgrounds/☠️ Success<br>`VariableID:40484:40768` | COLOR | → Brand/☠️ Success (`VariableID:37638:395909`) | → Brand/☠️ Success (`VariableID:37638:395909`) |
| Badge/Backgrounds/☠️ Accent<br>`VariableID:40484:40769` | COLOR | → Brand/☠️ Accent (`VariableID:37638:395908`) | → Brand/☠️ Accent (`VariableID:37638:395908`) |
| Badge/Backgrounds/☠️ Warning<br>`VariableID:40484:40770` | COLOR | → Brand/☠️ Warning (`VariableID:37638:395910`) | → Brand/☠️ Warning (`VariableID:37638:395910`) |
| Badge/Backgrounds/☠️ Danger<br>`VariableID:40484:40772` | COLOR | → Brand/☠️ Danger (`VariableID:37638:395911`) | → Brand/☠️ Danger (`VariableID:37638:395911`) |
| Badge/Text/☠️ Neutral<br>`VariableID:40484:40777` | COLOR | → Special/☠️ Ink (`VariableID:37662:395931`) | → Special/☠️ Ghost (`VariableID:37662:395932`) |
| Badge/Text/☠️ Inverse<br>`VariableID:40484:40779` | COLOR | → Plain/Light [внешняя] (`VariableID:ba65a7c5d7794d67a239ce8106a0d845baf75bda/9050:2663`) | → Plain/Dark [внешняя] (`VariableID:9e1494ba084245dad55810ebde635a36d72765bf/9050:2671`) |
| Badge/Text/☠️ Warning<br>`VariableID:40484:40782` | COLOR | → Warning/110 [внешняя] (`VariableID:022ce01c80006aa6dec39850fe9a9690afc5778b/9050:2100`) | → Warning/110 [внешняя] (`VariableID:022ce01c80006aa6dec39850fe9a9690afc5778b/9050:2100`) |
| Badge/Text/☠️ Disabled<br>`VariableID:40484:40784` | COLOR | → Text/☠️ Disabled (`VariableID:37641:395915`) | → Text/☠️ Disabled (`VariableID:37641:395915`) |
| Badge/Backgrounds/☠️ Accent (Alternative)<br>`VariableID:40484:40786` | COLOR | → Text/☠️ Accent (`VariableID:37641:395919`) | → Text/☠️ Accent (`VariableID:37641:395919`) |
| ＊ Elastic charts/☠️ Grid<br>`VariableID:43040:2` | COLOR | → Shades/20 [внешняя] (`VariableID:86623ddeef09b983254b4d9e7b6eb6534f87151c/9057:164`) | → Shades/120 [внешняя] (`VariableID:da64ee1fa24f067a5d6a5fd3b2153d1ce280d74d/9057:165`) |
| ＊ Elastic charts/☠️ Grid Label<br>`VariableID:43040:9241` | COLOR | → Shades/90 [внешняя] (`VariableID:fdee217e7916ece5bb2a2e74333b71d32a12e2ff/9057:86`) | → Shades/50 [внешняя] (`VariableID:57fb22988f28582273b1a47782c5b88e8fe242c4/9057:157`) |
| ＊ Elastic charts/☠️ Bullet Background<br>`VariableID:43040:16773` | COLOR | → Shades/10 [внешняя] (`VariableID:0a229da56861dc2aa851b9cab8694aad4a5dafe9/9057:119`) | → Shades/125 [внешняя] (`VariableID:de953176328f008d2265e7dff081d6fd39befda7/9057:144`) |
| Selectable/☠️ Option Border<br>`VariableID:43135:49113` | COLOR | → Shades/20 [внешняя] (`VariableID:86623ddeef09b983254b4d9e7b6eb6534f87151c/9057:164`) | → Shades/120 [внешняя] (`VariableID:da64ee1fa24f067a5d6a5fd3b2153d1ce280d74d/9057:165`) |
| Comment list/Borders/☠️ Primary<br>`VariableID:43196:311996` | COLOR | → Primary/30 [внешняя] (`VariableID:1ddfd35edca8f9131a1591b244f2ddc602fd095c/9072:33`) | → Primary/120 [внешняя] (`VariableID:82467654289699e7f0bd6e8c531299bb3a656ab1/9072:12`) |
| Loading/Chart/Mono/☠️ Color 1<br>`VariableID:43758:80851` | COLOR | → Shades/20 [внешняя] (`VariableID:86623ddeef09b983254b4d9e7b6eb6534f87151c/9057:164`) | → Shades/110 [внешняя] (`VariableID:a9ae13ab72c4c401acf042f58c265244a5df3771/9057:128`) |
| Loading/Chart/Mono/☠️ Color 2<br>`VariableID:43758:116980` | COLOR | → Shades/30 [внешняя] (`VariableID:e95997b50ac5a14eb10a05cac2eafab3d6cb4c8c/9057:124`) | → Shades/100 [внешняя] (`VariableID:8e4d08f8cc678569aa83b938727b0f29db556bc7/9057:112`) |
| Loading/Chart/Mono/☠️ Color 3<br>`VariableID:43758:116981` | COLOR | → Shades/40 [внешняя] (`VariableID:589fa4630215e61deb10b7990bb32e2f109fc59e/9057:154`) | → Shades/90 [внешняя] (`VariableID:fdee217e7916ece5bb2a2e74333b71d32a12e2ff/9057:86`) |
| Loading/Chart/Mono/☠️ Color 4<br>`VariableID:43758:116982` | COLOR | → Shades/50 [внешняя] (`VariableID:57fb22988f28582273b1a47782c5b88e8fe242c4/9057:157`) | → Shades/80 [внешняя] (`VariableID:e9839fe05d43b59074ccc67dd353da7bfb989749/9057:89`) |
| Color selection/Palette/☠️ Border<br>`VariableID:43774:228613` | COLOR | → Shades/20 [внешняя] (`VariableID:86623ddeef09b983254b4d9e7b6eb6534f87151c/9057:164`) | → Shades/120 [внешняя] (`VariableID:da64ee1fa24f067a5d6a5fd3b2153d1ce280d74d/9057:165`) |
| Skeleton/☠️ Gradient End<br>`VariableID:44385:1341` | COLOR | → Shades/100 (alpha)/16% [внешняя] (`VariableID:55715732b0d36c0689a77dbda57a3d424b28c733/9050:2166`) | → Plain/Light (alpha)/16% [внешняя] (`VariableID:500537792f7d2290d2445b69a910fe1fd5f0e2ce/9050:2675`) |
| Skeleton/☠️ Gradient Middle<br>`VariableID:44385:1342` | COLOR | → Shades/100 (alpha)/4% [внешняя] (`VariableID:df5a1e361636109d6ad7c03c896c8f99e68a67a2/9050:2124`) | → Plain/Light (alpha)/8% [внешняя] (`VariableID:ba7c0b2be6e8c72dbc7c88d102a4508f705379e6/9050:2672`) |
| Selection controls/Switch/Backgrounds/☠️ Disabled<br>`VariableID:44616:69542` | COLOR | → Shades/30 [внешняя] (`VariableID:e95997b50ac5a14eb10a05cac2eafab3d6cb4c8c/9057:124`) | → Shades/120 [внешняя] (`VariableID:da64ee1fa24f067a5d6a5fd3b2153d1ce280d74d/9057:165`) |
| Selection controls/Switch/Border/☠️ Thumb Disabled<br>`VariableID:44616:69543` | COLOR | → Shades/30 [внешняя] (`VariableID:e95997b50ac5a14eb10a05cac2eafab3d6cb4c8c/9057:124`) | → Shades/100 [внешняя] (`VariableID:8e4d08f8cc678569aa83b938727b0f29db556bc7/9057:112`) |
| Color selection/Swatch/☠️ Border<br>`VariableID:44709:22527` | COLOR | → Shades/100 (alpha)/24% [внешняя] (`VariableID:5abc68b6c46c5ef8e4b7ac1c1dd6caadbf9a2eaa/9050:2143`) | #FFFFFF; α=0.32 |
| Color selection/Swatch/☠️ Shadow<br>`VariableID:44709:22528` | COLOR | → Plain/Light (alpha)/8% [внешняя] (`VariableID:ba7c0b2be6e8c72dbc7c88d102a4508f705379e6/9050:2672`) | → Shades/100 (alpha)/4% [внешняя] (`VariableID:df5a1e361636109d6ad7c03c896c8f99e68a67a2/9050:2124`) |
| Popover/☠️ Background<br>`VariableID:44732:25304` | COLOR | → Plain/Light [внешняя] (`VariableID:ba65a7c5d7794d67a239ce8106a0d845baf75bda/9050:2663`) | → Shades/145 [внешняя] (`VariableID:23baad0b0275e1a3e243ad43cc53f754f72d2d9d/9057:168`) |
| Collapsible nav/☠️ Background<br>`VariableID:44994:27866` | COLOR | → Shades/130 [внешняя] (`VariableID:de3dbb603d7227e4043a4b5a3e6193175fe652cf/9057:155`) | → Plain/Dark [внешняя] (`VariableID:9e1494ba084245dad55810ebde635a36d72765bf/9050:2671`) |
| Collapsible nav/☠️ Text<br>`VariableID:44994:28000` | COLOR | → Plain/Light [внешняя] (`VariableID:ba65a7c5d7794d67a239ce8106a0d845baf75bda/9050:2663`) | → Plain/Light [внешняя] (`VariableID:ba65a7c5d7794d67a239ce8106a0d845baf75bda/9050:2663`) |
| Header/Dark/☠️ Input Placeholder<br>`VariableID:45055:745` | COLOR | → Shades/60 [внешняя] (`VariableID:2b37c2ffc9be925275ee5264486501323fd0af15/9057:121`) | → Shades/60 [внешняя] (`VariableID:2b37c2ffc9be925275ee5264486501323fd0af15/9057:121`) |
| Shadow/☠️ 1<br>`VariableID:45128:2134` | COLOR | #000000; α=0.03 | #000000; α=0.106 |
| Shadow/☠️ 2<br>`VariableID:45128:2135` | COLOR | #000000; α=0.04 | #000000; α=0.14 |
| Shadow/☠️ 3<br>`VariableID:45128:2136` | COLOR | #000000; α=0.05 | #000000; α=0.176 |
| Shadow/☠️ 4<br>`VariableID:45128:2137` | COLOR | #000000; α=0.06 | #000000; α=0.21 |
| Shadow/☠️ 5<br>`VariableID:45128:2138` | COLOR | #000000; α=0.07 | #000000; α=0.243 |
| Shadow/☠️ 6<br>`VariableID:45128:2139` | COLOR | #000000; α=0.08 | #000000; α=0.28 |
| Shadow/☠️ 7<br>`VariableID:45128:2140` | COLOR | #000000; α=0.09 | #000000; α=0.314 |
| Shadow/☠️ 8<br>`VariableID:45128:2141` | COLOR | #000000; α=0.1 | #000000; α=0.35 |
| Shadow/☠️ 9<br>`VariableID:45128:2142` | COLOR | #000000; α=0.13 | #000000; α=0.455 |
| Selection controls/Switch/Border/☠️ Thumb Off<br>`VariableID:48621:12488` | COLOR | → Shades/90 [внешняя] (`VariableID:fdee217e7916ece5bb2a2e74333b71d32a12e2ff/9057:86`) | → Shades/60 [внешняя] (`VariableID:2b37c2ffc9be925275ee5264486501323fd0af15/9057:121`) |
| Special/☠️ Floating<br>`VariableID:48647:199151` | COLOR | #FFFFFF; α=0 | → Shades/120 [внешняя] (`VariableID:da64ee1fa24f067a5d6a5fd3b2153d1ce280d74d/9057:165`) |
| Text/☠️ Risk<br>`VariableID:49521:33465` | COLOR | → Risk/110 [внешняя] (`VariableID:36ccdcd988e429533dcf73eedf2824449b168dd2/9265:10`) | → Risk/50 [внешняя] (`VariableID:9a53ea273f19e366d83578bdbdc951c4431ef505/9265:0`) |
| Text/☠️ Regular<br>`VariableID:49521:79574` | COLOR | → Neutral/100 [внешняя] (`VariableID:e8049c21605883164720dac7ee7682afe95e96b3/9667:8`) | → Neutral/60 [внешняя] (`VariableID:beb5d6caa57faf397ffa9bb068b4fb0c482785fa/9667:5`) |
| Backgrounds/Opaque/☠️ Risk<br>`VariableID:49521:79603` | COLOR | → Risk/10 [внешняя] (`VariableID:cf6f81f86f1dba29eff95d6c6cde9fbe4bf2cb48/9265:7`) | → Risk/140 [внешняя] (`VariableID:25e42c873535d51f21d310fdd7ce5c8661e5a681/9265:13`) |
| Backgrounds/Opaque/☠️ Regular<br>`VariableID:49521:79604` | COLOR | → Neutral/10 [внешняя] (`VariableID:21072fe94a7d65a2a881a870413a06178cc29023/9667:12`) | → Neutral/140 [внешняя] (`VariableID:d589210826a612aa65fce28d783dd081a3aa68a7/9667:13`) |
| Backgrounds/Transparent/☠️ Risk<br>`VariableID:49521:79613` | COLOR | → Backgrounds/Opaque/☠️ Risk (`VariableID:49521:79603`) | → Backgrounds/Opaque/☠️ Risk (`VariableID:49521:79603`) |
| Backgrounds/Transparent/☠️ Regular<br>`VariableID:49521:79614` | COLOR | → Backgrounds/Opaque/☠️ Regular (`VariableID:49521:79604`) | → Backgrounds/Opaque/☠️ Regular (`VariableID:49521:79604`) |
| Visualization palettes/Color blind/Severity/☠️ Unknown<br>`VariableID:49521:79615` | COLOR | → Shades/20 [внешняя] (`VariableID:86623ddeef09b983254b4d9e7b6eb6534f87151c/9057:164`) | → Shades/20 [внешняя] (`VariableID:86623ddeef09b983254b4d9e7b6eb6534f87151c/9057:164`) |
| Visualization palettes/Color blind/Severity/☠️ Success<br>`VariableID:49521:79616` | COLOR | → Success/60 [внешняя] (`VariableID:6406b6122d0d48fcf913522f013cfec7a1884d96/9050:2087`) | → Success/60 [внешняя] (`VariableID:6406b6122d0d48fcf913522f013cfec7a1884d96/9050:2087`) |
| Visualization palettes/Color blind/Severity/☠️ Regular<br>`VariableID:49521:79617` | COLOR | → Neutral/30 [внешняя] (`VariableID:bbad7e34c68a0e2d1df90779be0b4bcd120096bc/9667:2`) | → Neutral/30 [внешняя] (`VariableID:bbad7e34c68a0e2d1df90779be0b4bcd120096bc/9667:2`) |
| Visualization palettes/Color blind/Severity/☠️ Warning<br>`VariableID:49521:79618` | COLOR | → Warning/30 [внешняя] (`VariableID:c4a62faf5a8da618f28058c5753cb8f08d985acb/9050:2115`) | → Warning/30 [внешняя] (`VariableID:c4a62faf5a8da618f28058c5753cb8f08d985acb/9050:2115`) |
| Visualization palettes/Color blind/Severity/☠️ Risk<br>`VariableID:49521:79619` | COLOR | → Risk/50 [внешняя] (`VariableID:9a53ea273f19e366d83578bdbdc951c4431ef505/9265:0`) | → Risk/50 [внешняя] (`VariableID:9a53ea273f19e366d83578bdbdc951c4431ef505/9265:0`) |
| Visualization palettes/Color blind/Severity/☠️ Danger<br>`VariableID:49521:79620` | COLOR | → Danger/70 [внешняя] (`VariableID:320e3ab7c127668537aa892533deb9fad7c102b8/9050:2254`) | → Danger/70 [внешняя] (`VariableID:320e3ab7c127668537aa892533deb9fad7c102b8/9050:2254`) |
| Badge/Backgrounds/☠️ Risk<br>`VariableID:49521:79629` | COLOR | → Risk/70 [внешняя] (`VariableID:562849e1e4e064cfbacfb40a9ac4ca1c6e549d1b/9266:6`) | → Risk/50 [внешняя] (`VariableID:9a53ea273f19e366d83578bdbdc951c4431ef505/9265:0`) |
| Badge/Backgrounds/☠️ Regular<br>`VariableID:49521:79630` | COLOR | → Neutral/80 [внешняя] (`VariableID:358f51042f4c3fb49f2d0a2ba5304d1e262fbaba/9667:6`) | → Neutral/50 [внешняя] (`VariableID:e00c0752c7f9a0cfaefe17834486503cdb68edb0/9667:1`) |
| Badge/Text/☠️ Risk<br>`VariableID:49521:79641` | COLOR | #FFFFFF | #FFFFFF |
| Badge/Text/☠️ Regular<br>`VariableID:49521:79642` | COLOR | #FFFFFF | #FFFFFF |
| Button/Default/Backgrounds/☠️ Risk<br>`VariableID:49521:79643` | COLOR | → Risk/20 [внешняя] (`VariableID:1547be3bf33a2e96ce66de20ab05434987755eed/9265:2`) | → Risk/130 [внешняя] (`VariableID:48dc0cdb207ce378d8730e13b2695ada27938914/9265:11`) |
| Button/Default/Backgrounds/☠️ Regular<br>`VariableID:49521:79644` | COLOR | → Neutral/20 [внешняя] (`VariableID:8a159027c9487a50511adbfd5d7da8609c234f4e/9667:0`) | → Neutral/130 [внешняя] (`VariableID:2a4215913a308d4d5f3623445d41582dce2b70de/9667:11`) |
| Button/Default/Text/☠️ Risk<br>`VariableID:49521:79653` | COLOR | → Text/☠️ Risk (`VariableID:49521:33465`) | → Text/☠️ Risk (`VariableID:49521:33465`) |
| Button/Default/Text/☠️ Regular<br>`VariableID:49521:79654` | COLOR | → Text/☠️ Regular (`VariableID:49521:79574`) | → Text/☠️ Regular (`VariableID:49521:79574`) |
| Button/Filled/Backgrounds/☠️ Risk<br>`VariableID:49523:32` | COLOR | → Risk/60 [внешняя] (`VariableID:97fe20aa07c57d05a509e1c2c7c8e7c51fdb4418/9265:3`) | → Risk/50 [внешняя] (`VariableID:9a53ea273f19e366d83578bdbdc951c4431ef505/9265:0`) |
| Button/Filled/Backgrounds/☠️ Regular<br>`VariableID:49523:718` | COLOR | → Neutral/60 [внешняя] (`VariableID:beb5d6caa57faf397ffa9bb068b4fb0c482785fa/9667:5`) | → Neutral/50 [внешняя] (`VariableID:e00c0752c7f9a0cfaefe17834486503cdb68edb0/9667:1`) |
| Button/Filled/Text/☠️ Risk<br>`VariableID:49523:1750` | COLOR | → Risk/120 [внешняя] (`VariableID:52cc7847317400849b17ea917fb3c0320e74ac1e/9265:8`) | → Risk/120 [внешняя] (`VariableID:52cc7847317400849b17ea917fb3c0320e74ac1e/9265:8`) |
| Button/Filled/Text/☠️ Regular<br>`VariableID:49523:1797` | COLOR | → Neutral/120 [внешняя] (`VariableID:158475036d6ed1bfea46fb782ae7cff21ad3b0cd/9667:10`) | → Neutral/120 [внешняя] (`VariableID:158475036d6ed1bfea46fb782ae7cff21ad3b0cd/9667:10`) |
| Button/Empty/Text/☠️ Risk<br>`VariableID:49523:1814` | COLOR | → Button/Default/Text/☠️ Risk (`VariableID:49521:79653`) | → Button/Default/Text/☠️ Risk (`VariableID:49521:79653`) |
| Button/Empty/Text/☠️ Regular<br>`VariableID:49523:1815` | COLOR | → Button/Default/Text/☠️ Regular (`VariableID:49521:79654`) | → Button/Default/Text/☠️ Regular (`VariableID:49521:79654`) |
| Comment List/Backgrounds/☠️ Regular<br>`VariableID:49523:1816` | COLOR | → Button/Filled/Backgrounds/☠️ Regular (`VariableID:49523:718`) | → Button/Filled/Backgrounds/☠️ Regular (`VariableID:49523:718`) |
| Comment List/Backgrounds/☠️ Risk<br>`VariableID:49523:1817` | COLOR | → Button/Filled/Backgrounds/☠️ Risk (`VariableID:49523:32`) | → Button/Filled/Backgrounds/☠️ Risk (`VariableID:49523:32`) |
| Comment List/Text/☠️ Regular<br>`VariableID:49523:1818` | COLOR | → Button/Filled/Text/☠️ Regular (`VariableID:49523:1797`) | → Button/Filled/Text/☠️ Regular (`VariableID:49523:1797`) |
| Comment List/Text/☠️ Risk<br>`VariableID:49523:1819` | COLOR | → Button/Filled/Text/☠️ Risk (`VariableID:49523:1750`) | → Button/Filled/Text/☠️ Risk (`VariableID:49523:1750`) |

## Dimensions

Коллекция `VariableCollectionId:38581:395682`. Прочитано 21 / 21. Режим по умолчанию: Mode 1.

| Имя / Variable ID | Тип | Mode 1 |
| --- | --- | --- |
| Radius/Medium<br>`VariableID:38581:395683` | FLOAT | 6 |
| Radius/Small<br>`VariableID:38581:395684` | FLOAT | 4 |
| Button group/Compressed/Button/Radius<br>`VariableID:38581:395686` | FLOAT | 3 |
| Size/XX-Small<br>`VariableID:38809:395511` | FLOAT | 2 |
| Size/X-Small<br>`VariableID:38809:395512` | FLOAT | 4 |
| Size/Small<br>`VariableID:38809:395513` | FLOAT | 8 |
| Size/Medium<br>`VariableID:38809:395514` | FLOAT | 12 |
| Size/Base<br>`VariableID:38809:395515` | FLOAT | 16 |
| Size/Large<br>`VariableID:38809:395516` | FLOAT | 24 |
| Size/X-Large<br>`VariableID:38809:395517` | FLOAT | 32 |
| Size/XX-Large<br>`VariableID:38809:395518` | FLOAT | 40 |
| Size/XXX-Large<br>`VariableID:38809:395519` | FLOAT | 48 |
| Size/XXXX-Large<br>`VariableID:38809:395520` | FLOAT | 64 |
| Button/Minimum Width<br>`VariableID:38809:395521` | FLOAT | 112 |
| Button group/Compressed/Button/Height<br>`VariableID:38809:397545` | FLOAT | 26 |
| Button group/Compressed/Padding<br>`VariableID:38809:397552` | FLOAT | 3 |
| Badge/Height<br>`VariableID:40488:51240` | FLOAT | 20 |
| Badge/Radius<br>`VariableID:40488:51241` | FLOAT | 3 |
| Notfication badge/Medium/Height<br>`VariableID:40488:51244` | FLOAT | 20 |
| Beta badge/Small/Width<br>`VariableID:40488:51971` | FLOAT | 20 |
| Beta badge/Small/Height<br>`VariableID:40488:51972` | FLOAT | 20 |

## Typographic scale

Коллекция `VariableCollectionId:46681:1003`. Прочитано 21 / 21. Режим по умолчанию: Medium.

| Имя / Variable ID | Тип | Medium | Small | X-small |
| --- | --- | --- | --- | --- |
| Font family/Sans-serif (default)<br>`VariableID:46681:1004` | STRING | → Font family/Inter [внешняя] (`VariableID:10ff31c4e4340d09452b7c7d9f26a71d1885ee98/6407:505`) | → Font family/Inter [внешняя] (`VariableID:10ff31c4e4340d09452b7c7d9f26a71d1885ee98/6407:505`) | → Font family/Inter [внешняя] (`VariableID:10ff31c4e4340d09452b7c7d9f26a71d1885ee98/6407:505`) |
| Font family/Mono<br>`VariableID:46681:1005` | STRING | → Font family/Roboto Mono [внешняя] (`VariableID:54487534026640976dbc7881754a0164be91a546/6407:509`) | → Font family/Roboto Mono [внешняя] (`VariableID:54487534026640976dbc7881754a0164be91a546/6407:509`) | → Font family/Roboto Mono [внешняя] (`VariableID:54487534026640976dbc7881754a0164be91a546/6407:509`) |
| Font size/X-Small<br>`VariableID:46681:1006` | FLOAT | 12 | 10.5 | 9 |
| Font size/Small<br>`VariableID:46681:1007` | FLOAT | 14 | 12.25 | 10.5 |
| Font size/Medium<br>`VariableID:46681:1008` | FLOAT | 16 | 14 | 12 |
| Font size/Large<br>`VariableID:46681:1009` | FLOAT | 20 | 17.5 | 15 |
| Font size/X-Large<br>`VariableID:46681:1010` | FLOAT | 24 | 21 | 18 |
| Font size/XX-Large<br>`VariableID:46681:1011` | FLOAT | 30 | 26.25 | 22.5 |
| Line height/X-Small<br>`VariableID:46681:1012` | FLOAT | 16 | 16 | 12 |
| Line height/Small<br>`VariableID:46681:1013` | FLOAT | 20 | 16 | 16 |
| Line height/Medium<br>`VariableID:46681:1014` | FLOAT | 24 | 20 | 16 |
| Line height/Large<br>`VariableID:46681:1015` | FLOAT | 24 | 20 | 20 |
| Line height/X-Large<br>`VariableID:46681:1016` | FLOAT | 28 | 24 | 20 |
| Line height/XX-Large<br>`VariableID:46681:1017` | FLOAT | 36 | 32 | 28 |
| Font weight/Light<br>`VariableID:46681:1018` | FLOAT | → Font weight/Light [внешняя] (`VariableID:3315129b2a62c97d98e82350f711501677ceab86/6407:513`) | → Font weight/Light [внешняя] (`VariableID:3315129b2a62c97d98e82350f711501677ceab86/6407:513`) | → Font weight/Light [внешняя] (`VariableID:3315129b2a62c97d98e82350f711501677ceab86/6407:513`) |
| Font weight/Regular<br>`VariableID:46681:1019` | FLOAT | → Font weight/Regular [внешняя] (`VariableID:e54304c874a88cafc96f1232f873ff5e54a12be6/6407:517`) | → Font weight/Regular [внешняя] (`VariableID:e54304c874a88cafc96f1232f873ff5e54a12be6/6407:517`) | → Font weight/Regular [внешняя] (`VariableID:e54304c874a88cafc96f1232f873ff5e54a12be6/6407:517`) |
| Font weight/Medium<br>`VariableID:46681:1020` | FLOAT | → Font weight/Medium [внешняя] (`VariableID:8be8444c4a592f5acf1ba94446588ac69b590723/6407:521`) | → Font weight/Medium [внешняя] (`VariableID:8be8444c4a592f5acf1ba94446588ac69b590723/6407:521`) | → Font weight/Medium [внешняя] (`VariableID:8be8444c4a592f5acf1ba94446588ac69b590723/6407:521`) |
| Font weight/Semi Bold<br>`VariableID:46681:1021` | FLOAT | → Font weight/Semi bold [внешняя] (`VariableID:24a59002ee87b050dcae40a28d1f0696fdb23a5c/6407:525`) | → Font weight/Semi bold [внешняя] (`VariableID:24a59002ee87b050dcae40a28d1f0696fdb23a5c/6407:525`) | → Font weight/Semi bold [внешняя] (`VariableID:24a59002ee87b050dcae40a28d1f0696fdb23a5c/6407:525`) |
| Font weight/Bold<br>`VariableID:46681:1022` | FLOAT | → Font weight/Bold [внешняя] (`VariableID:2fe420da59ff4dbafeb6a3bde0bf3b21f23c403f/6407:529`) | → Font weight/Bold [внешняя] (`VariableID:2fe420da59ff4dbafeb6a3bde0bf3b21f23c403f/6407:529`) | → Font weight/Bold [внешняя] (`VariableID:2fe420da59ff4dbafeb6a3bde0bf3b21f23c403f/6407:529`) |
| Font size/Medium (Mono)<br>`VariableID:46681:1023` | FLOAT | 14.399999618530273 | 12.600000381469727 | 10.800000190734863 |
| Font style/Italic<br>`VariableID:46681:17263` | STRING | → Font style/Italic [внешняя] (`VariableID:972b01ecdd8f7964b9dff8de242a646bdea05876/6407:533`) | → Font style/Italic [внешняя] (`VariableID:972b01ecdd8f7964b9dff8de242a646bdea05876/6407:533`) | → Font style/Italic [внешняя] (`VariableID:972b01ecdd8f7964b9dff8de242a646bdea05876/6407:533`) |

## Типографика: локальные Text Styles

Это стили, а не отдельные Variables. Значения прочитаны плоским API без обхода текстов в компонентах. Привязки сохранены в index.json; цель вне текущего снимка не означает сломанную ссылку.

| Стиль | Шрифт | Размер / интерлиньяж | Style ID |
| --- | --- | --- | --- |
| ☠️ Headings (h1–h6)/☠️ Heading 1 | Inter / Semi Bold | 30 / {'unit': 'PIXELS', 'value': 36} | `S:99abb7ac5c806691680484bfcb99a18653882ebf,` |
| ☠️ Headings (h1–h6)/☠️ Heading 2 | Inter / Semi Bold | 24 / {'unit': 'PIXELS', 'value': 28} | `S:a0fb5401c910ccd1871625995412cdd09c8f0c3b,` |
| ☠️ Headings (h1–h6)/☠️ Heading 3 | Inter / Semi Bold | 20 / {'unit': 'PIXELS', 'value': 24} | `S:638cf4b32a8c492fa5e4cd6f99bfe69529e93a3d,` |
| ☠️ Headings (h1–h6)/☠️ Heading 4 | Inter / Semi Bold | 16 / {'unit': 'PIXELS', 'value': 24} | `S:638c665e238b8abfff2c7cf384d1c8643fa7e9da,` |
| ☠️ Headings (h1–h6)/☠️ Heading 5 | Inter / Semi Bold | 14 / {'unit': 'PIXELS', 'value': 20} | `S:e3675238f9b6ede89bd17e22419e8692d20909f2,` |
| ☠️ Headings (h1–h6)/☠️ Heading 6 | Inter / Semi Bold | 12 / {'unit': 'PIXELS', 'value': 16} | `S:0e404e4f2d95b07a23d7d7af842e95035f322d9d,` |
| ☠️ Body Copy (p)/☠️ Regular | Inter / Regular | 16 / {'unit': 'PIXELS', 'value': 24} | `S:055057128653b8e0591ad4af0f3f89ef9b2a5065,` |
| ☠️ Body Copy (p)/☠️ Regular, italic | Inter / Italic | 16 / {'unit': 'PIXELS', 'value': 24} | `S:dc5ae49f35b2c5525305a6baac76ee0da965c37a,` |
| ☠️ Body Copy (p)/☠️ Regular, underline | Inter / Regular | 16 / {'unit': 'PIXELS', 'value': 24} | `S:179c9870dcd15a416f275847824802b6400acbb5,` |
| ☠️ Body Copy (p)/☠️ Medium | Inter / Medium | 16 / {'unit': 'PIXELS', 'value': 24} | `S:f9812c3b501de2fc60a2086c9d855d94e3bd1950,` |
| ☠️ Body Copy (p)/☠️ Medium, underline | Inter / Medium | 16 / {'unit': 'PIXELS', 'value': 24} | `S:0d34d64860a8872bc63ee3bd95fa097cfa887e6b,` |
| ☠️ Body Copy (p)/☠️ Semi bold | Inter / Semi Bold | 16 / {'unit': 'PIXELS', 'value': 24} | `S:1d84bdc19179b2e8062cab3bde3b21ad2d066691,` |
| ☠️ Body Copy (p)/☠️ Semi bold, underline | Inter / Semi Bold | 16 / {'unit': 'PIXELS', 'value': 24} | `S:76484f4dca24057f5d46cfdd90cbcecb6820f7cd,` |
| ☠️ Body Copy (p)/☠️ Bold | Inter / Bold | 16 / {'unit': 'PIXELS', 'value': 24} | `S:52de9aeca99c0c9ac6b6d8d4b7d51fd3542db9b2,` |
| ☠️ Body Copy (p)/☠️ Bold, underline | Inter / Bold | 16 / {'unit': 'PIXELS', 'value': 24} | `S:dcbf479fb41f241dcad7fb26287425c00a8f2843,` |
| ☠️ Fine Print (small)/☠️ Regular | Inter / Regular | 14 / {'unit': 'PIXELS', 'value': 24} | `S:0ffe9932b31ce3305d4041a590cc8ec20d95f4d2,` |
| ☠️ Fine Print (small)/☠️ Regular, italic | Inter / Italic | 14 / {'unit': 'PIXELS', 'value': 24} | `S:7b509cd789fe20db7a94b4ce712c49acc9b15b9c,` |
| ☠️ Fine Print (small)/☠️ Regular, underline | Inter / Regular | 14 / {'unit': 'PIXELS', 'value': 24} | `S:c428eea4bb7846e4e25eba4b1064c01d7ed740be,` |
| ☠️ Fine Print (small)/☠️ Medium | Inter / Medium | 14 / {'unit': 'PIXELS', 'value': 24} | `S:1e8c22b826e029e5595a772fa39f887b29b9d2d3,` |
| ☠️ Fine Print (small)/☠️ Medium, underline | Inter / Medium | 14 / {'unit': 'PIXELS', 'value': 24} | `S:03587740797433b373aa828dfe82614982dd94ff,` |
| ☠️ Fine Print (small)/☠️ Semi bold | Inter / Semi Bold | 14 / {'unit': 'PIXELS', 'value': 24} | `S:2cd4b6374aea1f83a864466cb5b5d6bf3f7c155b,` |
| ☠️ Fine Print (small)/☠️ Semi bold, underline | Inter / Semi Bold | 14 / {'unit': 'PIXELS', 'value': 24} | `S:681eab4aa1dca4f9bb4fbd969a1f9d2d5f8fe767,` |
| ☠️ Fine Print (small)/☠️ Bold | Inter / Bold | 14 / {'unit': 'PIXELS', 'value': 24} | `S:2fb91864ac84186025883e0f5dcab7453672e0d6,` |
| ☠️ Fine Print (small)/☠️ Bold, underline | Inter / Bold | 14 / {'unit': 'PIXELS', 'value': 24} | `S:8ae571eb356e1bbabe59098df3de8d16a9718f65,` |
| ☠️ Link (a)/☠️ Default | Inter / Medium | 16 / {'unit': 'PIXELS', 'value': 24} | `S:6b3e7fa1adeb4f9b58ec3f8d48efc3b4775453d7,` |
| ☠️ Link (a)/☠️ Hover | Inter / Medium | 16 / {'unit': 'PIXELS', 'value': 24} | `S:c3c699fdedd4ad0776386a2e18ae65f26017432c,` |
| ☠️ Mono (code)/☠️ Regular | Roboto Mono / Regular | 14.399999618530273 / {'unit': 'PIXELS', 'value': 24} | `S:0984a48b790120b9e37889f886315d9381507421,` |
| ☠️ Mono (code)/☠️ Regular, italic | Roboto Mono / Italic | 14.399999618530273 / {'unit': 'PIXELS', 'value': 24} | `S:76cff9fd2efa3a37c5ac5cf5bab92e12dfe11bad,` |
| ☠️ Mono (code)/☠️ Bold | Roboto Mono / Bold | 14.399999618530273 / {'unit': 'PIXELS', 'value': 24} | `S:7df4374dbdd2b7f0c15774e78903abbd37f31bb9,` |

## Замечания

- Дубликаты имён Variables внутри одной коллекции: не обнаружены в прочитанной части.
- Alias локальных переменных сохранены; 102 целей находятся во внешних библиотеках (remote=true), имена проверены. Цепочки внешних значений не разворачивались.
- Неопознанных целей alias локальных Variables: 0. Все локальные значения и режимы получены; внешние зависимости явно помечены.
- Использование токенов в компонентах не проверено: для этого потребовался бы запрещённый директивой глубокий обход.
- Поддержка кириллицы конкретными версиями Inter и Roboto Mono в этом файле не проверена. Перед финальной типографикой проверить Щ/Ъ/Ь/Ы и русский текст; не подменять проверку названием семейства.
- Text Styles с меткой ☠️: 29 из 29. Статус требует проверки; метка сама по себе не заменяет описание автора.
- Собственные цвета: следующий этап — согласовать палитру и семантическое соответствие, затем адаптировать токены. Не перекрашивать инстансы по одному. Цвета состояний и шкала тепловой карты требуют отдельного смыслового соответствия, не механической замены акцента.

## Foundation продукта в Dashboard — 2026-09-22

[Foundation](https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=82-15) находится рядом с UI Kit — extended на странице UX-Lab · UI Kit. Исходный снимок Elastic UI выше сохранён.

Используются импортированные Body Copy/Regular, Body Copy/Medium, Fine Print/Regular (Inter); новых Text Styles не создано. Их fontFamily, fontSize, fontWeight и lineHeight связаны с Variables. Размеры импортированы из Dimensions: 4, 8, 12, 16, 24, 32; радиус Radius/Small — 4. Цвета — существующая палитра продукта.

Добавлена отдельная коллекция UX-Lab · Heatmap: 10 semantic-переменных heatmap/intensity/1…10, режим Light, scopes FRAME_FILL и SHAPE_FILL, WEB code syntax. Шкала светлый → тёмный оливковый — проектное решение для легенды. Алгоритм агрегации, числовые пороги и шкала реальных данных не утверждены. Полные значения и Node ID сохранены в productExtensions файла index.json и grow-ui-kit-audit.json.

Это целевая основа трёх дополнений; полный перенос или модернизация всех 204 исходных элементов не выполнялись.


## Красный ползунок — 22 сентября 2026

`replay/playhead` = `#C61E25` (VariableID:102:94). Цвет пользователя сохранён; линия и кружок всех четырёх вариантов ReplayControls привязаны к отдельному токену позиции воспроизведения. Цвета ошибок и маркеров событий не менялись. Эта правка заменяет прежнее описание оливкового ползунка.


## Состояния взаимодействий — 22 сентября 2026

Пять semantic aliases ссылаются на существующие базовые цвета продукта. Новые цветовые значения не создавались.

| Token | Alias | Figma ID |
| --- | --- | --- |
| action/hover | text/primary | `VariableID:125:154` |
| action/pressed | text/secondary | `VariableID:125:155` |
| surface/hover | background/sidebar | `VariableID:125:156` |
| surface/pressed | accent/soft | `VariableID:125:157` |
| border/focus | accent/strong | `VariableID:125:158` |

Focus — отдельная обводка 2 px, не цвет ошибки; Selected обозначен поверхностью и полосой/подчёркиванием. Disabled — opacity 0.4. Размеры контролов сохранены между состояниями.

<!-- final-results-shadow -->
## Радиусы крупных поверхностей · 23 сентября 2026

По указанию пользователя увеличено скругление карточек, таблиц и крупных плашек. Semantic `radius/surface` (`VariableID:202:3805`) ссылается на Primitive `radius/12` (`VariableID:202:3804`): **12 px**. Применён к SummaryMetric, ScenarioTable, ParticipantsTable, FirstClickTargets, DataCoverage, ReplayControls и HeatmapLegend. Компактные кнопки и поля сохраняют прежний радиус. Новые крупные поверхности финальных экранов используют `radius/surface`.

## Тень карточки · final_screens

- Primitive `black/4%`: RGBA(0,0,0,0.04), `VariableID:171:1757`, коллекция `UX-Lab · Primitives` (`VariableCollectionId:171:1756`). Scope пустой; CSS `var(--black-4-percent)`.
- Semantic `shadow/color`: alias к black/4%, `VariableID:171:1758`, scope EFFECT_COLOR; CSS `var(--shadow-color)`.
- Effect Style `shadow/card`, ID `S:33899efc313cd34c3be9f04a04d0853ed7091433,`: x=0, y=2, blur=8, spread=0. Цвет эффекта связан с shadow/color. Применён к SummaryMetric.
- Внешний исходный Plain/Dark не удалось импортировать, поэтому создан локальный примитив согласованного чёрного 4%. Цвета существующих контролов не менялись.

<!-- thermal-final-2026-09-23 -->
## Цветовая шкала тепловой карты · 23 сентября 2026

По прямому указанию пользователя прежняя оливковая шкала заменена на **жёлтую → оранжевую → красную**, как в wireframe `22:101` (пятна `57:3`). Это шкала данных, а не фирменный акцент.
`heatmap/intensity/1…10` теперь aliases к отдельным thermal-примитивам: #FFF8DF, #FFF0B8, #FFE788, #FFDB36, #FFC630, #FFAC29, #FF8C22, #F77323, #ED5525, #E33C26.
Радиальный слой: core #E33C26 / 70%, middle #FF8C22 / 56%, outer #FFDA36 / 30%, edge #FFDF38 / 0%. Позиции: 0, 0.36, 0.72, 1.
Идентификаторы, scopes, aliases и codeSyntax прочитаны из Figma: [thermal-radius-tokens.json](thermal-radius-tokens.json).
Три финальных режима карты и HeatmapLegend синхронизированы. Алгоритм плотности и числовые границы шкалы не выведены из демонстрационных пятен.

<!-- secondary-approved-2026-09-23 -->
## Secondary · выбран A без обводки

23 сентября 2026 пользователь утвердил образец A `237:11664` без контура. Все шесть состояний ProductButton Secondary обновлены, включая локальные заливки на страницах. Обычный фон — `action/secondary/background` #E4E5DC, Hover — `action/secondary/hover` #D8DACD, Pressed — `action/secondary/pressed` #CCD0BE. Семантика ссылается на отдельные neutral/secondary primitives; общий border/subtle не менялся.

Контур появляется только при клавиатурном фокусе; Disabled сохраняет opacity 0.4. Оливковые выбранные режимы и скорости сохранены. Primary и Tertiary не изменялись. Исторические варианты B/C/D и прежняя доска сравнения сохраняют собственные настройки.

Проверены 7 страниц: 378 обычных Secondary-контролов соответствуют новому стилю, устаревших применений среди них нет. На Final Screens — 248 контролов; проверка геометрии и привязок всех 55 экранов пройдена. [Аудит и токены](secondary-choice-audit.json).

<!-- logo-token-2026-09-23 -->
## Логотип

Пользовательский Logo 289:13519: вектор связан с существующим text/inverse (VariableID:67:115), цвет визуально сохранён. ProductMark использует существующий фон action/primary. Новые цветовые значения не создавались.
