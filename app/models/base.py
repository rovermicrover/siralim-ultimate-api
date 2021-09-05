class BaseModelOrm(object):
  @classmethod
  def from_orm_list(model, orm_list):
    return [ model.from_orm(orm) for orm in orm_list ]