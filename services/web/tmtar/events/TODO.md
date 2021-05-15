# TODO

##  model
If you need, you could add this to model, but it makes no sense to segregate users by age or gender.

It'll be better to abandon this features
```python
    sex = db.Column(db.String, default=SexType[2])
    min_age = db.Column(db.Integer, default=0)
    max_age = db.Column(db.Integer, default=150)
```