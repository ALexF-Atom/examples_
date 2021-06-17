from typing import Any, Dict, Type
import re


class ImageRichFieldMeta(Type):
    def __getitem__(self, params: Any) -> Type['ImageRichField']:
        return type('ImageRichFieldValue', (ImageRichField,),
                    # {'params': params}
                    )


class ColorsListBackgroundMeta(Type):
    def __getitem__(self, params: Any) -> Type['ColorsListBackground']:
        return type('ColorsListBacgkroundValue', (ColorsListBackground,),
                    # {'params': params}
                    )


class AnswerDataMeta(Type):
    def __getitem__(self, params: Any) -> Type['AnswerData']:
        return type('AnswerData', (AnswerData,),
                    # {'params': params}
                    )


class ImageRichField(metaclass=ImageRichFieldMeta):
    allowed_schemes = {'http', 'https'}
    # params: Any = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if v is None:
            return ""
        if re.match('http', v):
            return v
        if (res := re.findall(r'(?=src)src=\"(?P<src>[^\"]+)', v)):
            return res[0]
        return v

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(
            type='string', format='uri')


class ColorsListBackground(metaclass=ColorsListBackgroundMeta):
    allowed_schemes = {'http', 'https'}
    # params: Any = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if v:
            return v.split(',')
        return v

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(
            type='List', format='uri')


class AnswerData(metaclass=AnswerDataMeta):
    allowed_schemes = {'http', 'https'}
    # params: Any = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):

        if v:
            v = [{
                'answer': item[0],
                'answer_colors': item[1].split(',') if item[1] else None,
                'answer_vector': item[2],
                'text_color': item[3],
                'order': item[4]
            }
                for item in v]

        return v

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(
            type='List', format='uri')
