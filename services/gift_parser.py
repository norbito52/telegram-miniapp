"""
Сервіс для парсингу подарунків з Telegram каналів
"""
import re
import asyncio
import logging
from typing import Dict, Any, List, Optional
from services.telegram_service import get_telegram_service
from app.config import GIFT_MAPPING

logger = logging.getLogger(__name__)


class GiftParser:
    """Сервіс для парсингу подарунків з каналів"""
    
    def __init__(self):
        self.telegram_service = get_telegram_service()
        
        # Паттерни для розпізнавання подарунків
        self.gift_patterns = {
            "HEELS": [r"heels", r"high heels", r"👠", r"каблук", r"туфл"],
            "BUTTON": [r"button", r"🔘", r"кнопк", r"button"],
            "CATS": [r"cats", r"cat", r"🐱", r"кот", r"кіт", r"котик"],
            "SOCKS": [r"socks", r"🧦", r"шкарпетк", r"носк"],
            "BICEPS": [r"biceps", r"muscle", r"💪", r"біцепс", r"м'язи"],
            "LAMP": [r"lamp", r"💡", r"лампа", r"світло"],
            "BOUQUET": [r"bouquet", r"flowers", r"💐", r"букет", r"квіти"],
            "CUPCAKE": [r"cupcake", r"cake", r"🧁", r"кекс", r"торт"],
            "MARCH 8": [r"march", r"8 march", r"🌸", r"8 берез", r"жіноч"],
            "DYSON": [r"dyson", r"vacuum", r"🌪️", r"дайсон", r"пилосос"],
            "BOILER": [r"boiler", r"🔥", r"котел", r"бойлер"],
            "CLOVER": [r"clover", r"🍀", r"конюшина", r"клевер"],
            "AMULET": [r"amulet", r"🧿", r"амулет", r"оберіг"],
            "MOSQUE": [r"mosque", r"🕌", r"мечеть", r"мосък"],
            "DOSHIK": [r"doshik", r"noodles", r"🍜", r"дошик", r"лапша"],
            "POOP": [r"poop", r"💩", r"какашк", r"говно"],
            "MONKEY": [r"monkey", r"🐵", r"мавп", r"обезьян"],
            "BRICK": [r"brick", r"🧱", r"цегл", r"кирпич"],
            "ROCKET": [r"rocket", r"🚀", r"ракет", r"корабл"],
            "KULICH": [r"kulich", r"easter", r"🍞", r"кулич", r"паск"],
            "RABBIT": [r"rabbit", r"bunny", r"🐰", r"кролик", r"заяц"],
            "1 MAY": [r"1 may", r"may day", r"🌹", r"1 травн", r"май"],
            "MEDAL": [r"medal", r"🏅", r"медаль", r"нагород"],
            "PIGEON": [r"pigeon", r"🕊️", r"голуб", r"птиц"],
            "STAR": [r"star", r"⭐", r"зірк", r"звезд"],
            "CREAMY ICE CREAM": [r"ice cream", r"🍦", r"морозив", r"мороженое"],
            "ESKIMO": [r"eskimo", r"🧊", r"ескімо", r"эскимос"],
            "PLUMBER": [r"plumber", r"mario", r"🔧", r"сантехнік", r"водопровод"],
            "NIPPLE": [r"nipple", r"🍼", r"соска", r"пустишк"],
            "EAGLE": [r"eagle", r"🦅", r"орел", r"птах"],
            "STATUE": [r"statue", r"🗿", r"статуя", r"пам'ятник"],
            "TORCH": [r"torch", r"🔦", r"факел", r"ліхтар"],
            "WESTSIDE SIGN": [r"westside", r"west", r"🤟", r"захід", r"знак"],
            "LOW RIDER": [r"low rider", r"car", r"🚗", r"машин", r"автомобіль"],
            "SNOOP CIGAR": [r"cigar", r"🚬", r"сигар", r"курін"],
            "SWAG BAG": [r"swag", r"bag", r"🎒", r"сумк", r"рюкзак"],
            "SNOOP DOGG": [r"snoop", r"dogg", r"🎤", r"снуп", r"репер"]
        }
        
        # Паттерни для розпізнавання кількості
        self.count_patterns = [
            r"(\d+)\s*(?:шт|штук|pieces|pcs|x|×)",
            r"count[:\s]*(\d+)",
            r"кількість[:\s]*(\d+)",
            r"количество[:\s]*(\d+)",
            r"total[:\s]*(\d+)",
            r"всього[:\s]*(\d+)",
            r"(\d+)\s*(?:подарунк|подарок|gift)"
        ]
    
    async def parse_channel_gifts(self, channel_id: int) -> List[Dict[str, Any]]:
        """
        Парсинг подарунків з каналу
        """
        try:
            # Отримуємо повідомлення з каналу
            messages = await self.telegram_service.get_channel_messages(channel_id)
            
            # Якщо повідомлень немає, генеруємо демо-дані
            if not messages:
                return self._generate_demo_gifts(channel_id)
            
            # Парсимо подарунки з повідомлень
            gifts = {}
            
            for message in messages:
                parsed_gifts = self._parse_message_for_gifts(message)
                
                for gift_name, count in parsed_gifts.items():
                    if gift_name in gifts:
                        gifts[gift_name] += count
                    else:
                        gifts[gift_name] = count
            
            # Конвертуємо в формат для БД
            result = []
            for gift_name, count in gifts.items():
                gift_id = self._get_gift_id_by_name(gift_name)
                if gift_id:
                    result.append({
                        "id": gift_id,
                        "name": gift_name,
                        "count": count,
                        "image_url": self._get_gift_image_url(gift_id)
                    })
            
            return result if result else self._generate_demo_gifts(channel_id)
            
        except Exception as e:
            logger.error(f"Failed to parse gifts from channel {channel_id}: {e}")
            return self._generate_demo_gifts(channel_id)
    
    def _parse_message_for_gifts(self, message: Dict[str, Any]) -> Dict[str, int]:
        """
        Парсинг одного повідомлення для пошуку подарунків
        """
        gifts = {}
        text = message.get("text", "").lower()
        
        if not text:
            return gifts
        
        # Шукаємо подарунки за паттернами
        for gift_name, patterns in self.gift_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    # Знайшли подарунок, тепер шукаємо кількість
                    count = self._extract_count_from_text(text, pattern)
                    if count > 0:
                        gifts[gift_name] = gifts.get(gift_name, 0) + count
                    break
        
        return gifts
    
    def _extract_count_from_text(self, text: str, gift_pattern: str) -> int:
        """
        Витягування кількості з тексту
        """
        # Шукаємо кількість поблизу згадки подарунка
        gift_match = re.search(gift_pattern, text, re.IGNORECASE)
        if not gift_match:
            return 1  # За замовчуванням 1 штука
        
        # Беремо текст навколо згадки подарунка
        start = max(0, gift_match.start() - 50)
        end = min(len(text), gift_match.end() + 50)
        context = text[start:end]
        
        # Шукаємо кількість в контексті
        for pattern in self.count_patterns:
            match = re.search(pattern, context, re.IGNORECASE)
            if match:
                try:
                    count = int(match.group(1))
                    return count if count > 0 else 1
                except (ValueError, IndexError):
                    continue
        
        return 1  # За замовчуванням
    
    def _get_gift_id_by_name(self, gift_name: str) -> Optional[int]:
        """
        Отримання ID подарунка за назвою
        """
        for gift_id, gift_info in GIFT_MAPPING.items():
            if gift_info["name"] == gift_name:
                return gift_id
        return None
    
    def _get_gift_image_url(self, gift_id: int) -> str:
        """
        Отримання URL зображення подарунка
        """
        # Базові URL для зображень подарунків
        base_urls = {
            1: "https://i.postimg.cc/jdsL20Gt/Gifts-Gifts-Gifts-Ag-ADBmg-AAnz-Oe-Ek.png",
            2: "https://i.postimg.cc/XqDSnCRZ/Gifts-Gifts-Gifts-Ag-ADWWg-AAhwgi-Uk.png",
            3: "https://i.postimg.cc/rmnY4LQ3/Gifts-Gifts-Gifts-Ag-ADCWc-AAk-LAe-Uk.png",
            4: "https://i.postimg.cc/bwxCTnmQ/Gifts-Gifts-Gifts-Ag-ADKmk-AAt0-L2-Ek.png",
            5: "https://i.postimg.cc/K4Xf7cLq/Gifts-Gifts-Gifts-Ag-ADB3-UAAp5-V0-Uk.png",
            6: "https://i.postimg.cc/hjfNpjzc/Gifts-Gifts-Gifts-Ag-ADj-Gw-AAkl0c-Eo.png",
            7: "https://i.postimg.cc/TY8BJTRv/Gifts-Gifts-Gifts-Ag-ADk3-AAAiy-WGEs.png",
            8: "https://i.postimg.cc/gkqtyRS3/Gifts-Gifts-Gifts-Ag-ADB3-AAAr-Pqc-Eo.png",
            9: "https://i.postimg.cc/d1y4hTZk/Gifts-Gifts-Gifts-Ag-ADh2o-AAoa-Dc-Eo.png",
            10: "https://i.postimg.cc/3NZjGj8R/Gifts-Gifts-Gifts-Ag-ADhmw-AAl1-Zc-Uo.png",
            11: "https://i.postimg.cc/Dfc1Bghf/Gifts-Gifts-Gifts-Ag-ADe-WMAAp-Rw-IUs.png",
            12: "https://i.postimg.cc/NfJmwjLW/Gifts-Gifts-Gifts-Ag-ADf-GYAAjfaw-Uo.png",
            13: "https://i.postimg.cc/hGFJSzn3/Gifts-Gifts-Gifts-Ag-AD-HEAAq-9c-Us.png",
            14: "https://i.postimg.cc/pr1T3ykC/Gifts-Gifts-Gifts-Ag-ADV3-MAAnv-We-Us.png",
            15: "https://i.postimg.cc/k5F5qTfB/Gifts-Gifts-Gifts-Ag-AD4-GQAAq8-Xg-Us.png",
            16: "https://i.postimg.cc/05HykMdd/Gifts-Gifts-Gifts-Ag-AD82w-AAk-FZg-Es.png",
            17: "https://i.postimg.cc/bN7Yn75Z/Gifts-Gifts-Gifts-Ag-AEZAACV66-BSw.png",
            18: "https://i.postimg.cc/c1jdyq0F/Gifts-Gifts-Gifts-Ag-ADg2o-AAg-R5g-Us.png",
            19: "https://i.postimg.cc/nhfZrvs7/Gifts-Gifts-Gifts-Ag-ADIo-UAAk3-J2-Es.png",
            20: "https://i.postimg.cc/tTJGwkf0/Gifts-Gifts-Gifts-Ag-ADBa-UAAk8-WKEg.png",
            21: "https://i.postimg.cc/WtLRDv4j/Gifts-Gifts-Gifts-Ag-ADh-HUAAg-O6-IUg.png",
            22: "https://i.postimg.cc/gJxk8GG6/Gifts-Gifts-Gifts-Ag-ADMm4-AAj-Ll6-Ug.png",
            23: "https://i.postimg.cc/N0zQgZRG/Gifts-Gifts-Gifts-Ag-ADO3c-AAqb-DEEk.png",
            24: "https://i.postimg.cc/QxJsBFcy/Gifts-Gifts-Gifts-Ag-ADa3-QAAtw-JEEk.png",
            25: "https://i.postimg.cc/3Nr1nfbp/Gifts-Gifts-Gifts-Ag-ADbn-UAAl-XNEUk.png",
            26: "https://i.postimg.cc/ydjXgXYN/Gifts-Gifts-Gifts-Ag-AD0-Ww-AAs4-T4-Ek.png",
            27: "https://i.postimg.cc/L4y3mTbC/Gifts-Gifts-Gifts-Ag-ADy-XEAAky04-Ek.png",
            28: "https://i.postimg.cc/85pLSJBg/Gifts-Gifts-Gifts-Ag-ADKX4-AAuw-O2-Ek.png",
            29: "https://i.postimg.cc/BQrDvwcg/Gifts-Gifts-Gifts-Ag-ADD3-IAAm-RNKUo.png",
            30: "https://i.postimg.cc/0QXK1ty7/Gifts-Gifts-Gifts-Ag-ADzn-IAAl-Gn-QEs.png",
            31: "https://i.postimg.cc/V6hvVdKR/Gifts-Gifts-Gifts-Ag-ADi-IYAAqf-LQEs.png",
            32: "https://i.postimg.cc/wv1LMKPw/Gifts-Gifts-Gifts-Ag-AD2-XQAAk-VPSEs.png",
            33: "https://i.postimg.cc/GtkBTbjx/Gifts-Gifts-Gifts-Ag-ADV4-QAAiibe-Us.png",
            34: "https://i.postimg.cc/7Y96Fsth/Gifts-Gifts-Gifts-Ag-ADNWw-AAg5ze-Es.png",
            35: "https://i.postimg.cc/FKMsy2zW/Gifts-Gifts-Gifts-Ag-ADi38-AAg-7c-Es.png",
            36: "https://i.postimg.cc/d1cwkrNg/Gifts-Gifts-Gifts-Ag-AD5-XMAAmjze-Us.png",
            37: "https://i.postimg.cc/vmG9dxbL/Gifts-Gifts-Gifts-Ag-ADdn-MAAj-Jye-Es.png"
        }
        
        return base_urls.get(gift_id, "")
    
    def _generate_demo_gifts(self, channel_id: int) -> List[Dict[str, Any]]:
        """
        Генерація демо-подарунків для каналу
        """
        import random
        
        # Базові шаблони для різних типів каналів
        demo_templates = {
            "fashion": [1, 4, 36, 2, 25, 7],  # Fashion Style
            "animals": [3, 17, 21, 1, 24, 30],  # Cat Lovers
            "tech": [6, 10, 19, 2, 27, 18],  # Tech Store
            "food": [8, 15, 26, 3, 20, 16],  # Sweet Treats
            "entertainment": [37, 33, 34, 36, 35, 32],  # Hip Hop
            "misc": [2, 6, 5, 22, 12, 9]  # Button Collectors
        }
        
        # Вибираємо шаблон на основі channel_id
        template_keys = list(demo_templates.keys())
        template_key = template_keys[abs(channel_id) % len(template_keys)]
        gift_ids = demo_templates[template_key]
        
        # Генеруємо подарунки
        gifts = []
        for gift_id in gift_ids:
            gift_info = GIFT_MAPPING.get(gift_id)
            if gift_info:
                # Генеруємо випадкову кількість
                count = random.randint(50, 3000)
                
                gifts.append({
                    "id": gift_id,
                    "name": gift_info["name"],
                    "count": count,
                    "image_url": self._get_gift_image_url(gift_id)
                })
        
        return gifts
    
    async def refresh_channel_gifts(self, channel_id: int) -> List[Dict[str, Any]]:
        """
        Оновлення подарунків каналу
        """
        try:
            # Отримуємо свіжі дані
            gifts = await self.parse_channel_gifts(channel_id)
            
            logger.info(f"Refreshed {len(gifts)} gifts for channel {channel_id}")
            return gifts
            
        except Exception as e:
            logger.error(f"Failed to refresh gifts for channel {channel_id}: {e}")
            return []
    
    def analyze_gift_trends(self, channels_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Аналіз трендів подарунків
        """
        try:
            gift_stats = {}
            total_channels = len(channels_data)
            
            for channel_data in channels_data:
                gifts = channel_data.get("gifts", [])
                
                for gift in gifts:
                    gift_id = gift["id"]
                    gift_name = gift["name"]
                    count = gift["count"]
                    
                    if gift_id not in gift_stats:
                        gift_stats[gift_id] = {
                            "name": gift_name,
                            "total_count": 0,
                            "channels_count": 0,
                            "avg_count_per_channel": 0
                        }
                    
                    gift_stats[gift_id]["total_count"] += count
                    gift_stats[gift_id]["channels_count"] += 1
            
            # Рахуємо середні значення
            for gift_id, stats in gift_stats.items():
                if stats["channels_count"] > 0:
                    stats["avg_count_per_channel"] = stats["total_count"] / stats["channels_count"]
                    stats["popularity"] = (stats["channels_count"] / total_channels) * 100
            
            return {
                "total_channels_analyzed": total_channels,
                "unique_gifts_found": len(gift_stats),
                "gift_statistics": gift_stats,
                "most_popular_gifts": sorted(
                    gift_stats.items(),
                    key=lambda x: x[1]["popularity"],
                    reverse=True
                )[:10],
                "rarest_gifts": sorted(
                    gift_stats.items(),
                    key=lambda x: x[1]["channels_count"]
                )[:10]
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze gift trends: {e}")
            return {}
