from .inline.ais_keyboards import (gen_ai_types_kb, gen_img_model_kb,
                                   gen_main_video_kb, gen_text_models_kb,
                                   gen_text_roles_kb, gen_txt_settings_kb)
from .inline.common_keyboards import gen_error_kb
from .inline.midjourney_keyboards import gen_midjourney_kb
from .inline.payments_keyboards import gen_no_tokens_kb, gen_premium_kb
from .inline.profile_keyboards import gen_profile_kb
from .inline.silero_keyboards import (gen_main_speaker_kb,
                                      gen_speaker_category_kb)
from .reply.main_keyboard import main_kb
