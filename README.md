# Miknaaz مكناز

## Description

Generate Arabic golden standard corpus for morphology and stemming 

### Citation

If you would cite it in academic work, can you use this citation

	Taha Zerrouki‏, Miknaaz,  http://github.com/linuxscout/miknaaz, 2023

or in bibtex format

	@misc{zerrouki2018miknaaz,
	  title={Miknaaz: Generate arabic golden standard},
	  author={Zerrouki, Taha},
	  url={http://github.com/linuxscout/miknaaz},
	  year={2018}
	}

## Usage

* Build word features for linguistics building corpus

```python
from miknaaz.corpus_builder import CorpusBuilder
text = u"إلى البيت"
lemmer = CorpusBuilder()
words = lemmer.tokenize(text)
for word in words:
    result = lemmer.morph_suggestions(word, True)
    print(result)
```



* Extract separate features

  ```python
  from miknaaz.corpus_builder import CorpusBuilder
  text = u"إلى البيت"
  lemmer = CorpusBuilder()
  words = lemmer.tokenize(text)
  # test get lemmas
  for word in words:
      result = lemmer.get_lemmas(word)
      # the result contains objects
      print(result)
  # test get roots
  for word in words:
      result = lemmer.get_roots(word)
      # the result contains objects
      print(result)
  # test get wordtypes
  for word in words:
      result = lemmer.get_word_type(word)
      # the result contains objects
      print(result)
  # test get wazns
  for word in words:
      result = lemmer.get_wazns(word)
      # the result contains objects
      print(result)
  ```

  
